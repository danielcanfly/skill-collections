"""Load skill manifests and companion markdown files from disk.

The loader is intentionally simple:
- manifests are parsed from YAML
- instructions/examples/eval notes are read as plain text
- no network access is required at startup
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class SkillDefinition:
    name: str
    manifest: dict[str, Any]
    instructions: str
    examples: str
    eval_notes: str
    path: Path

    @property
    def allowed_backend_tools(self) -> list[str]:
        return list(self.manifest.get("allowed_backend_tools", []))


class SkillLoader:
    def __init__(self, skills_root: Path) -> None:
        self.skills_root = skills_root

    def load_all(self) -> dict[str, SkillDefinition]:
        if not self.skills_root.exists():
            raise FileNotFoundError(f"Skills root not found: {self.skills_root}")

        definitions: dict[str, SkillDefinition] = {}
        for child in sorted(self.skills_root.iterdir()):
            if not child.is_dir():
                continue
            definition = self._load_skill(child)
            definitions[definition.name] = definition
        return definitions

    def _load_skill(self, skill_dir: Path) -> SkillDefinition:
        manifest_path = skill_dir / "manifest.yaml"
        instructions_path = skill_dir / "instructions.md"
        examples_path = skill_dir / "examples.md"
        eval_notes_path = skill_dir / "eval-notes.md"

        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ValueError(f"Manifest must parse to a mapping: {manifest_path}")

        name = str(manifest.get("name") or skill_dir.name)
        return SkillDefinition(
            name=name,
            manifest=manifest,
            instructions=instructions_path.read_text(encoding="utf-8"),
            examples=examples_path.read_text(encoding="utf-8"),
            eval_notes=eval_notes_path.read_text(encoding="utf-8"),
            path=skill_dir,
        )

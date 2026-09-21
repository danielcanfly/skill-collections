from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_markdown(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.startswith("---\n") and "\n---\n" in text[4:]:
        raw, body = text[4:].split("\n---\n", 1)
        if yaml is not None:
            try:
                return yaml.safe_load(raw) or {}, body
            except Exception:
                pass
        return parse_simple_frontmatter(raw), body
    return {}, text


def parse_simple_frontmatter(raw: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    current_list: str | None = None
    for line in raw.splitlines():
        if re.match(r"^\s+-\s+", line) and current_list:
            out.setdefault(current_list, []).append(re.sub(r"^\s+-\s+", "", line).strip().strip("'\""))
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        current_list = None
        if value == "":
            out[key] = []
            current_list = key
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            out[key] = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
        elif value.lower() in {"true", "false"}:
            out[key] = value.lower() == "true"
        else:
            out[key] = value.strip("'\"")
    return out


def strip_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[`*_>#|]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_text(text: str) -> str:
    text = strip_markdown(text).lower()
    text = re.sub(r"\b(?:[a-z]{2,}-)?(?:concept|claim|source|case|edge|bind)-?[a-z0-9_-]+\b", " id ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def glob_many(root: Path, patterns: Iterable[str]) -> list[Path]:
    found: set[Path] = set()
    for pattern in patterns:
        found.update(p for p in root.glob(pattern) if p.is_file())
    return sorted(found)


def ensure_relative(root: Path, value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else root / p


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "pass", "passed"}

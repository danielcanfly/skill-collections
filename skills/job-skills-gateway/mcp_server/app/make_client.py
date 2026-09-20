from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass(frozen=True, slots=True)
class MakeConfig:
    fetch_recent_jobs_url: str | None = os.getenv("MAKE_FETCH_RECENT_JOBS_URL")
    bulk_score_new_jobs_url: str | None = os.getenv("MAKE_BULK_SCORE_NEW_JOBS_URL")
    query_jobs_url: str | None = os.getenv("MAKE_QUERY_JOBS_URL")
    generate_job_output_url: str | None = os.getenv("MAKE_GENERATE_JOB_OUTPUT_URL")
    resolve_job_reference_url: str | None = os.getenv("MAKE_RESOLVE_JOB_REFERENCE_URL")
    timeout_seconds: float = float(os.getenv("MAKE_TIMEOUT_SECONDS", "45"))
    auth_header_value: str | None = os.getenv("MAKE_AUTH_HEADER_VALUE")


class MakeClientError(RuntimeError):
    pass


class MakeClient:
    def __init__(self, config: MakeConfig | None = None) -> None:
        self.config = config or MakeConfig()

    async def fetch_recent_jobs(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._post(self.config.fetch_recent_jobs_url, payload)

    async def bulk_score_new_jobs(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._post(self.config.bulk_score_new_jobs_url, payload)

    async def query_jobs(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._post(self.config.query_jobs_url, payload)

    async def generate_job_output(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._post(self.config.generate_job_output_url, payload)

    async def resolve_job_reference(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._post(self.config.resolve_job_reference_url, payload)

    async def _post(self, url: str | None, payload: dict[str, Any]) -> dict[str, Any]:
        if not url:
            raise MakeClientError("Make endpoint is not configured.")

        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self.config.auth_header_value:
            headers["x-make-apikey"] = self.config.auth_header_value

        response: httpx.Response | None = None
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
        except httpx.TimeoutException as exc:
            raise MakeClientError("Make request timed out.") from exc
        except httpx.HTTPStatusError as exc:
            raise MakeClientError(f"Make request returned HTTP {exc.response.status_code}.") from exc
        except ValueError as exc:
            snippet = ""
            if response is not None:
                snippet = response.text[:200]
            detail = f" Response body starts with: {snippet!r}" if snippet else ""
            raise MakeClientError(f"Make response was not valid JSON.{detail}") from exc

        if not isinstance(data, dict):
            raise MakeClientError("Make response JSON was not an object.")
        return data

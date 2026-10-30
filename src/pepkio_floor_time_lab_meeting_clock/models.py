# SPDX-License-Identifier: MIT
"""Typed API request/response models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from .exceptions import PepkioAPIError


class Participant(BaseModel):
    """Lab meeting participant definition."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    weight: float = 1.0


class FloorTimeInput(BaseModel):
    """Typed input helper for floor-time-lab-meeting-clock actions."""

    model_config = ConfigDict(extra="allow")

    action: str
    participants: list[Participant] | None = None
    total_minutes: float | None = None
    qa_buffer_minutes: float | None = None
    equal_split: bool | None = None
    carryover: bool | None = None
    soft_chime: bool | None = None
    slots: list[dict[str, Any]] | None = None
    actual_seconds: dict[str, int | float] | None = None
    url_hash: str | None = None
    origin: str | None = None
    pathname: str | None = None


class RunOptions(BaseModel):
    """Optional fields for POST .../run."""

    idempotency_key: str | None = None
    label: str | None = None


class RunResult(BaseModel):
    """Tool run response envelope."""

    model_config = ConfigDict(extra="allow")

    run_id: str
    status: str
    result: dict[str, Any] | None = None
    error: dict[str, Any] | str | None = None
    result_url: str | None = None
    permalink: str | None = None
    duration_ms: int | None = None

    def raise_for_error(self) -> None:
        """Raise PepkioAPIError if the run response includes an error field."""
        if self.error is None:
            return
        err = self.error
        if isinstance(err, str):
            raise PepkioAPIError(
                err,
                response_body={
                    "run_id": self.run_id,
                    "status": self.status,
                    "error": self.error,
                },
            )
        raise PepkioAPIError(
            err.get("message", "Tool run failed"),
            code=err.get("code"),
            details=err.get("details") if isinstance(err.get("details"), dict) else {},
            response_body={"run_id": self.run_id, "status": self.status, "error": self.error},
        )


def parse_run_response(data: dict[str, Any]) -> RunResult:
    """Parse a run API JSON body into RunResult."""
    return RunResult.model_validate(data)

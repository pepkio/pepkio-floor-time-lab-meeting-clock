"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load monorepo .env for local integration runs (never log keys).
_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "schema_version": "1.0",
        "tool_id": "floor-time-lab-meeting-clock",
        "title": "Floor Time — Lab Meeting Clock",
        "description": "Browser-only meeting clock that splits speaking time fairly.",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "compute_equal_split",
                "input": {
                    "action": "compute_allocations",
                    "participants": [
                        {"id": "1", "name": "Alice", "weight": 1},
                        {"id": "2", "name": "Bob", "weight": 1},
                        {"id": "3", "name": "Carol", "weight": 1},
                    ],
                    "total_minutes": 30,
                    "qa_buffer_minutes": 5,
                    "equal_split": True,
                },
                "output": {"qa_buffer_seconds": 300},
            },
            {
                "name": "shuffle_participants",
                "input": {
                    "action": "shuffle",
                    "participants": [
                        {"id": "1", "name": "Alice", "weight": 1},
                        {"id": "2", "name": "Bob", "weight": 1},
                    ],
                },
                "output": {},
            },
            {
                "name": "validate_setup",
                "input": {
                    "action": "validate_setup",
                    "participants": [{"id": "1", "name": "Alice", "weight": 1}],
                    "total_minutes": 30,
                    "qa_buffer_minutes": 0,
                    "equal_split": True,
                },
                "output": {"valid": True},
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "slots": [
                {"id": "1", "name": "Alice", "allocatedSeconds": 750},
                {"id": "2", "name": "Bob", "allocatedSeconds": 750},
                {"id": "__qa__", "name": "Group Q&A", "allocatedSeconds": 300, "isQaBuffer": True},
            ],
            "qa_buffer_seconds": 300,
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }

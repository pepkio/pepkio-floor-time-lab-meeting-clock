"""Integration tests against live Pepkio Tools API (local and production)."""

from __future__ import annotations

import os

import pytest

from pepkio_floor_time_lab_meeting_clock.client import PepkioClient

# Local first, then production (param order).
ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY") or os.getenv("PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


@pytest.fixture(params=ENVIRONMENTS, ids=["local", "production"])
def live_client(request):
    env_name, default_base_url = request.param
    base_url = os.getenv("PEPKIO_API_BASE_URL") or default_base_url
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")
    with PepkioClient(api_key=api_key, base_url=base_url) as client:
        yield client


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "floor-time-lab-meeting-clock"
    names = live_client.list_examples()
    assert "compute_equal_split" in names
    assert "shuffle_participants" in examples if (examples := names) else False


def test_run_compute_equal_split_example(live_client: PepkioClient):
    inp = live_client.get_example_input("compute_equal_split")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert result.result.get("qa_buffer_seconds") == 300
    assert isinstance(result.result.get("slots"), list)
    assert result.result.get("error") is None


def test_run_shuffle_participants_example(live_client: PepkioClient):
    inp = live_client.get_example_input("shuffle_participants")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.result is not None
    assert isinstance(result.result.get("participants"), list)
    assert len(result.result["participants"]) == 3


def test_run_validate_setup_example(live_client: PepkioClient):
    inp = live_client.get_example_input("validate_setup")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("valid") is True


def test_run_build_summary_csv_example(live_client: PepkioClient):
    inp = live_client.get_example_input("build_summary_csv")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("filename") == "floor-time-summary.csv"
    assert isinstance(result.result.get("content"), str)

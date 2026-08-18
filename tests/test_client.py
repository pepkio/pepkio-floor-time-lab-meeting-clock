"""Unit tests for PepkioClient with mocked HTTP responses."""

from __future__ import annotations

import json

import httpx
import pytest
from click.testing import CliRunner

from pepkio_floor_time_lab_meeting_clock.cli import main
from pepkio_floor_time_lab_meeting_clock.client import PepkioClient
from pepkio_floor_time_lab_meeting_clock.exceptions import PepkioAPIError


def test_missing_api_key_raises_error(monkeypatch):
    monkeypatch.delenv("PEPKIO_API_KEY", raising=False)
    monkeypatch.delenv("LOCAL_PEPKIO_API_KEY", raising=False)
    client = PepkioClient(api_key=None, base_url="https://tools.pepkio.com")
    with pytest.raises(ValueError, match="API key required"):
        client.run({"action": "compute_allocations"})


def test_get_manifest(mock_manifest):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/tools/v1/tools/floor-time-lab-meeting-clock/manifest":
            return httpx.Response(200, json=mock_manifest)
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com")
    client._http = httpx.Client(base_url="https://tools.pepkio.com", transport=transport)

    manifest = client.get_manifest()
    assert manifest["tool_id"] == "floor-time-lab-meeting-clock"

    # Test cache
    manifest_cached = client.get_manifest()
    assert manifest_cached is manifest

    # Test list_examples
    examples = client.list_examples()
    assert "compute_equal_split" in examples
    assert "shuffle_participants" in examples

    # Test get_example_input
    inp = client.get_example_input("compute_equal_split")
    assert inp["action"] == "compute_allocations"

    with pytest.raises(PepkioAPIError, match="Example not found"):
        client.get_example_input("non_existent_example")


def test_run_success(mock_run_response):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/tools/v1/tools/floor-time-lab-meeting-clock/run":
            body = json.loads(request.content)
            assert body["input"]["action"] == "compute_allocations"
            assert body["options"]["label"] == "test_run"
            return httpx.Response(200, json=mock_run_response)
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com")
    client._http = httpx.Client(base_url="https://tools.pepkio.com", transport=transport)

    result = client.run(
        {"action": "compute_allocations", "total_minutes": 30},
        label="test_run",
    )
    assert result.status == "completed"
    assert result.run_id == "run_test123"
    assert result.result["qa_buffer_seconds"] == 300


def test_run_error_response():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            json={
                "error": {
                    "message": "Invalid action",
                    "code": "INVALID_INPUT",
                    "details": {"field": "action"},
                }
            },
        )

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com")
    client._http = httpx.Client(base_url="https://tools.pepkio.com", transport=transport)

    with pytest.raises(PepkioAPIError) as exc_info:
        client.run({"action": "invalid_action"})

    err = exc_info.value
    assert err.status_code == 400
    assert err.code == "INVALID_INPUT"
    assert "Invalid action" in str(err)


def test_get_run_and_wait_for_run(mock_run_response):
    poll_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal poll_count
        if request.url.path == "/api/tools/v1/runs/run_test123":
            poll_count += 1
            if poll_count == 1:
                return httpx.Response(200, json={"run_id": "run_test123", "status": "running"})
            return httpx.Response(200, json=mock_run_response)
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com")
    client._http = httpx.Client(base_url="https://tools.pepkio.com", transport=transport)

    result = client.wait_for_run("run_test123", poll_interval=0.01, timeout=1.0)
    assert result.status == "completed"
    assert poll_count == 2


def test_cli_manifest(mock_manifest):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=mock_manifest)

    runner = CliRunner()
    with pytest.MonkeyPatch.context() as mp:
        def mock_client_factory(*args, **kwargs):
            c = PepkioClient(api_key="test", base_url="https://tools.pepkio.com")
            c._http = httpx.Client(
                base_url="https://tools.pepkio.com",
                transport=httpx.MockTransport(handler),
            )
            return c

        mp.setattr("pepkio_floor_time_lab_meeting_clock.cli._client", mock_client_factory)

        res = runner.invoke(main, ["manifest", "--examples"])
        assert res.exit_code == 0
        assert "compute_equal_split" in res.output

        res_full = runner.invoke(main, ["manifest"])
        assert res_full.exit_code == 0
        parsed = json.loads(res_full.output)
        assert parsed["tool_id"] == "floor-time-lab-meeting-clock"


def test_cli_run(mock_run_response, mock_manifest):
    def handler(request: httpx.Request) -> httpx.Response:
        if "/manifest" in request.url.path:
            return httpx.Response(200, json=mock_manifest)
        if "/run" in request.url.path:
            return httpx.Response(200, json=mock_run_response)
        return httpx.Response(404)

    runner = CliRunner()
    with pytest.MonkeyPatch.context() as mp:
        def mock_client_factory(*args, **kwargs):
            c = PepkioClient(api_key="test", base_url="https://tools.pepkio.com")
            c._http = httpx.Client(
                base_url="https://tools.pepkio.com",
                transport=httpx.MockTransport(handler),
            )
            return c

        mp.setattr("pepkio_floor_time_lab_meeting_clock.cli._client", mock_client_factory)

        # Run with example
        res = runner.invoke(main, ["run", "--example", "compute_equal_split"])
        assert res.exit_code == 0
        assert "run_test123" in res.output

        # Run with input-json
        res_json = runner.invoke(
            main, ["run", "--input-json", '{"action": "compute_allocations"}']
        )
        assert res_json.exit_code == 0
        assert "run_test123" in res_json.output

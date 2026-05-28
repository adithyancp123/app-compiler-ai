"""Compile endpoint contract and deterministic behavior tests."""

from fastapi.testclient import TestClient

from app.main import app


def test_compile_endpoint_contract() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/compile", json={"prompt": "Build a CRM with login and payments"})
    assert response.status_code == 200

    body = response.json()
    assert "stage_outputs" in body
    assert "validation_report" in body
    assert "simulation_result" in body
    assert body["generated_schema"]["ui"]["pages"]


def test_compile_deterministic_output() -> None:
    client = TestClient(app)
    payload = {"prompt": "Build CRM with login and payments"}
    response_a = client.post("/api/v1/compile", json=payload)
    response_b = client.post("/api/v1/compile", json=payload)

    assert response_a.status_code == 200
    assert response_b.status_code == 200

    body_a = response_a.json()
    body_b = response_b.json()

    assert body_a["generated_schema"] == body_b["generated_schema"]
    assert body_a["stage_outputs"][0]["content"] == body_b["stage_outputs"][0]["content"]

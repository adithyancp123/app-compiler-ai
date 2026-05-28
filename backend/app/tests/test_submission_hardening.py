"""Final submission hardening tests."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_vague_prompt_generates_clarification_or_assumption() -> None:
    response = client.post('/api/v1/compile', json={'prompt': 'Build an app for my business'})
    assert response.status_code == 200
    body = response.json()
    assert body['clarification_questions'] or body['assumptions']


def test_conflicting_prompt_detected() -> None:
    response = client.post('/api/v1/compile', json={'prompt': 'Everyone is admin but admins only can view analytics'})
    assert response.status_code == 200
    body = response.json()
    constraints = body['stage_outputs'][0]['content']['constraints']
    assert any('conflict' in item.lower() for item in constraints)


def test_incomplete_hospital_prompt_infers_entities() -> None:
    response = client.post('/api/v1/compile', json={'prompt': 'Build hospital app'})
    assert response.status_code == 200
    entities = response.json()['stage_outputs'][0]['content']['entities']
    assert 'patient' in entities
    assert 'appointment' in entities


def test_export_endpoints() -> None:
    payload = {'prompt': 'Build CRM with premium billing'}
    json_export = client.post('/api/v1/compile/export/json', json=payload)
    md_export = client.post('/api/v1/compile/export/markdown', json=payload)
    bench_json = client.get('/api/v1/evaluation/export/json')
    bench_md = client.get('/api/v1/evaluation/export/markdown')

    assert json_export.status_code == 200
    assert md_export.status_code == 200
    assert bench_json.status_code == 200
    assert bench_md.status_code == 200
    assert 'application/json' in json_export.headers['content-type']
    assert bench_md.text.startswith('# Benchmark Report')

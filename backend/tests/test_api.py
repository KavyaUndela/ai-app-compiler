from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get('/api/health')
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'healthy'
    assert payload['service'] == 'ai-application-compiler'


def test_generate_endpoint_returns_completed_compilation() -> None:
    response = client.post(
        '/api/generate',
        json={
            'prompt': 'Build a CRM with login, contacts, dashboard, role-based access, premium plans and payments.'
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'completed'
    assert payload['validation']['is_valid'] is True
    assert payload['intent']['entities']
    assert payload['schema']['database_schema']
    assert payload['runtime_preview']['dynamic_forms']


def test_validate_and_preview_endpoints() -> None:
    generated = client.post(
        '/api/generate',
        json={
            'prompt': 'Build a CRM with login, contacts, dashboard, role-based access, premium plans and payments.'
        },
    ).json()
    validate_response = client.post('/api/validate', json=generated['schema'])
    assert validate_response.status_code == 200
    assert validate_response.json()['is_valid'] is True

    preview_response = client.post('/api/runtime-preview', json={'schema': generated['schema']})
    assert preview_response.status_code == 200
    assert preview_response.json()['dynamic_forms']

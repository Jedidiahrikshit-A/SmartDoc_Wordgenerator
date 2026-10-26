import io
import os
import tempfile

import pytest

from backend.app import create_app, db, User, Document


@pytest.fixture()
def client():
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    app = create_app({
        'TESTING': True,
        'SECRET_KEY': 'test-secret',
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{path}',
        'SESSION_COOKIE_SECURE': False,
    })
    with app.test_client() as client:
        client.get('/api/auth/csrf')
        yield client
    os.remove(path)


def headers(client):
    token = client.get_cookie('csrf_token').value
    return {'X-CSRF-Token': token}


def register(client, email='alex@example.com'):
    return client.post('/api/auth/register', json={'name': 'Alex Morgan', 'email': email, 'password': 'strong-pass-123'}, headers=headers(client))


def test_register_duplicate_login_logout(client):
    assert register(client).status_code == 201
    assert register(client).status_code == 409
    assert client.get('/api/auth/me').status_code == 200
    assert client.post('/api/auth/logout', headers=headers(client)).status_code == 200
    assert client.post('/api/auth/login', json={'email': 'alex@example.com', 'password': 'strong-pass-123'}, headers=headers(client)).status_code == 200


def test_document_crud_and_ownership(client):
    register(client)
    created = client.post('/api/documents', json={'title': 'Proposal', 'document_type': 'Project proposal', 'content': '<p>Hello</p>'}, headers=headers(client))
    assert created.status_code == 201
    doc_id = created.get_json()['document']['id']
    assert client.put(f'/api/documents/{doc_id}', json={'content': '<h2>Updated</h2>'}, headers=headers(client)).status_code == 200
    assert client.get('/api/documents').get_json()['pagination']['total'] == 1
    assert client.post(f'/api/documents/{doc_id}/duplicate', json={}, headers=headers(client)).status_code == 201
    assert client.delete(f'/api/documents/{doc_id}', headers=headers(client)).status_code == 200


def test_exports_and_invalid_upload(client):
    register(client)
    created = client.post('/api/documents', json={'title': 'Export me', 'content': '<h1>Heading</h1><p>Paragraph.</p>'}, headers=headers(client))
    doc_id = created.get_json()['document']['id']
    assert client.get(f'/api/documents/{doc_id}/export/docx').status_code == 200
    assert client.get(f'/api/documents/{doc_id}/export/pdf').status_code == 200
    bad = client.post('/api/files/extract', data={'file': (io.BytesIO(b'no'), 'payload.exe')}, content_type='multipart/form-data', headers=headers(client))
    assert bad.status_code == 400


def test_missing_ai_credentials_is_honest(client, monkeypatch):
    register(client)
    monkeypatch.delenv('MANUS_API_URL', raising=False)
    monkeypatch.delenv('MANUS_API_KEY', raising=False)
    response = client.post('/api/ai/generate', json={'document_type': 'Resume', 'title': 'My resume'}, headers=headers(client))
    assert response.status_code == 503
    assert 'not configured' in response.get_json()['error']['message']


def test_auth_required(client):
    assert client.get('/api/documents').status_code == 401

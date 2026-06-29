import os
import tempfile
from fastapi.testclient import TestClient

from Backend.app import app
from Backend.db import initialize_database

client = TestClient(app)


def test_signup_and_login():
    initialize_database()
    response = client.post('/api/signup', json={'email': 'test@example.com', 'password': 'secret'})
    assert response.status_code == 200
    assert response.json()['message'] == 'Signup successful'

    response = client.post('/api/login', json={'email': 'test@example.com', 'password': 'secret'})
    assert response.status_code == 200
    assert 'token' in response.json()


def test_protected_chat_requires_auth():
    response = client.post('/api/chat', json={'question': 'What is flower care?'})
    assert response.status_code == 401


def test_status_endpoint():
    response = client.get('/api/status')
    assert response.status_code == 200
    json_data = response.json()
    assert json_data['status'] in {'ok', 'unhealthy'}
    assert 'database' in json_data


def test_upload_validation():
    initialize_database()
    signup = client.post('/api/signup', json={'email': 'upload@example.com', 'password': 'secret'})
    login = client.post('/api/login', json={'email': 'upload@example.com', 'password': 'secret'})
    token = login.json()['token']
    response = client.post(
        '/api/upload',
        files={'file': ('flower.txt', b'not-an-image', 'text/plain')},
        headers={'Authorization': f'Bearer {token}', 'X-User-Email': 'upload@example.com'},
    )
    assert response.status_code == 400


def test_chat_rag_route():
    initialize_database()
    client.post('/api/signup', json={'email': 'rag@example.com', 'password': 'secret'})
    login = client.post('/api/login', json={'email': 'rag@example.com', 'password': 'secret'})
    token = login.json()['token']
    response = client.post(
        '/api/chat',
        json={'question': 'How do I care for roses?'},
        headers={'Authorization': f'Bearer {token}', 'X-User-Email': 'rag@example.com'},
    )
    assert response.status_code == 200
    assert response.json()['source'] in {'rag', 'direct'}

import pytest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app

@pytest.fixture
def app():
    # Simular conexiones Redis y MySQL
    with patch("app.get_db_connection"), patch("app.get_redis_connection"):
        yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Registro' in response.data

def test_home_page_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.location

def test_valid_email():
    from app import valid_email
    assert valid_email('test@example.com') is not None
    assert valid_email('invalid-email') is None

def test_health_check(client):
    response = client.get('/login')
    assert response.status_code == 200

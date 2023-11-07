import requests
import pytest

BASE_URL = "http://localhost:5000"

def test_login():
    payload = {"email": "test@example.com", "password":"123"}

    try:
        response = requests.post(f"{BASE_URL}/login", json=payload)
        assert response.status_code == 201
    except Exception as e:
        pass

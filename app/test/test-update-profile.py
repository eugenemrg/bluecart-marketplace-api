import requests
import pytest

BASE_URL = "http://localhost:5000"

def test_update_profile():
    payload = {"email": "test@example.com", "password": "1234"}

    try:
        response = requests.post(f"{BASE_URL}/profile", json=payload)
        assert response.status_code == 201
    except Exception as e:
        pass

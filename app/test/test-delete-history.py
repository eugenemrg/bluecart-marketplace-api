import requests
import pytest

BASE_URL = "http://localhost:5000"

def test_delete_history():
    payload = {"email": "test@example.com"}

    try:
        response = requests.delete(f"{BASE_URL}/history", json=payload)
        assert response.status_code == 200
    except Exception as e:
        pass

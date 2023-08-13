from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json().get("message") == "Hello world"


def test_create_user():
    res = client.post("/users/", json={"email": "new_user@gmail.com", "password": "password123"})
    assert res.status_code == 201
    assert res.json().get("email") == "new_user@gmail.com"

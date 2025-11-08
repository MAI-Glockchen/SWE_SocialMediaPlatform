import pytest
from fastapi.testclient import TestClient
from app.main import app, init_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()

def test_create_post():
    post_data = {"image": "cat.png", "text": "Hello world", "user": "alice"}
    r = client.post("/posts/", json=post_data)
    assert r.status_code == 200
    data = r.json()
    assert data["user"] == "alice"
    assert "created_at" in data

def test_get_last_post():
    r = client.get("/posts/last")
    assert r.status_code == 200
    data = r.json()
    assert data["text"] == "Hello world"

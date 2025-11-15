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


def test_get_all_posts():
    r = client.get("/posts/")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Check that all expected keys are there
    assert "id" in data[0]
    assert "user" in data[0]
    assert "image" in data[0]
    assert "text" in data[0]
    assert "created_at" in data[0]


def test_get_post_by_id():
    # first POST a post so that I can GET it afterwords
    post_data = {"image": "dog.png", "text": "Test post", "user": "bob"}
    r = client.post("/posts/", json=post_data)
    post_id = r.json()["id"]

    # GET POST by id
    r2 = client.get(f"/posts/{post_id}")
    assert r2.status_code == 200
    data = r2.json()
    assert data["id"] == post_id
    assert data["user"] == "bob"
    assert data["text"] == "Test post"


def test_get_post_not_found():
    non_existent_id = 9999991231232351
    r = client.get(f"/posts/{non_existent_id}")
    assert r.status_code == 404
    data = r.json()
    assert data["detail"] == "Post not found"


def test_create_multiple_posts_and_get_all():
    for i in range(3):
        post_data = {"image": f"img{i}.png", "text": f"Post {i}", "user": f"user{i}"}

        client.post("/posts/", json=post_data)

    r = client.get("/posts/")
    data = r.json()
    assert len(data) >= 3

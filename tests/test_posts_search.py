import pytest
from fastapi.testclient import TestClient

from app.main import app, init_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()


def test_search_posts_by_text():
    # Create posts to search
    r1 = client.post(
        "/posts/", json={"image": "dog.png", "text": "Search test 123 ", "user": "bob"}
    )
    assert r1.status_code == 200, f"Failed to create post: {r1.text}"

    r = client.get("/posts/", params={"text": "Search test 123"})
    assert r.status_code == 200, f"Search request failed: {r.text}"

    data = r.json()
    assert len(data) > 0, "Search returned no results"

    for post in data:
        assert "Search" in post["text"], f"Post did not match search query: {post}"


def test_search_posts_by_user():
    # Search for posts by user "alice"
    r = client.get("/posts/", params={"user": "alice"})
    assert r.status_code == 200
    data = r.json()
    assert all(post["user"] == "alice" for post in data)
    assert len(data) > 0


def test_search_posts_by_text_and_user():
    # Create a post with known text and user
    client.post(
        "/posts/",
        json={"image": "img.png", "text": "UniqueText123456", "user": "unique_user"},
    )

    # Search by both
    r = client.get(
        "/posts/", params={"text": "UniqueText123456", "user": "unique_user"}
    )
    assert r.status_code == 200
    data = r.json()
    assert data[0]["user"] == "unique_user"
    assert "UniqueText123456" in data[0]["text"]


def test_search_no_results():
    r = client.get("/posts/", params={"text": "doesnotexist", "user": "nouser"})
    assert r.status_code == 404
    data = r.json()
    assert data["detail"] == "No posts found"

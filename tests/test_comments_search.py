import pytest
from fastapi.testclient import TestClient

from app.main import app, init_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()


def test_create_comment_for_post():
    # Create a post first
    post_data = {"image": "post.png", "text": "Post for comments", "user": "alice"}
    r = client.post("/posts/", json=post_data)
    assert r.status_code == 200
    post_id = r.json()["id"]

    # Create a comment
    comment_data = {"text": "Hello comment", "user": "bob"}
    r2 = client.post(f"/posts/{post_id}/comments", json=comment_data)
    assert r2.status_code == 200
    data = r2.json()
    assert data["user"] == "bob"
    assert "text" in data
    assert data["text"] == "Hello comment"


def test_search_comments_by_text():
    # Create comments
    post_data = {"image": "post2.png", "text": "Another post", "user": "alice"}
    post_id = client.post("/posts/", json=post_data).json()["id"]

    client.post(f"/posts/{post_id}/comments", json={"text": "FindMe123", "user": "bob"})
    client.post(
        f"/posts/{post_id}/comments", json={"text": "Other comment", "user": "charlie"}
    )

    # Search by text
    r = client.get(f"/posts/{post_id}/comments", params={"text": "FindMe123"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert "FindMe123" in data[0]["text"]


def test_search_comments_by_user():
    post_data = {"image": "post3.png", "text": "Yet another post", "user": "alice"}
    post_id = client.post("/posts/", json=post_data).json()["id"]

    client.post(
        f"/posts/{post_id}/comments", json={"text": "Comment1", "user": "user123"}
    )
    client.post(
        f"/posts/{post_id}/comments", json={"text": "Comment2", "user": "user123"}
    )
    client.post(
        f"/posts/{post_id}/comments", json={"text": "Comment3", "user": "otheruser"}
    )

    # Search by user
    r = client.get(f"/posts/{post_id}/comments", params={"user": "user123"})
    assert r.status_code == 200
    data = r.json()
    assert all(comment["user"] == "user123" for comment in data)
    assert len(data) == 2


def test_search_comments_by_text_and_user():
    post_data = {"image": "post4.png", "text": "Post for combo test", "user": "alice"}
    post_id = client.post("/posts/", json=post_data).json()["id"]

    client.post(
        f"/posts/{post_id}/comments",
        json={"text": "UniqueTextComment", "user": "unique_user"},
    )
    client.post(
        f"/posts/{post_id}/comments",
        json={"text": "UniqueTextComment", "user": "other_user"},
    )

    # Search by text + user
    r = client.get(
        f"/posts/{post_id}/comments",
        params={"text": "UniqueTextComment", "user": "unique_user"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data[0]["user"] == "unique_user"
    assert "UniqueTextComment" in data[0]["text"]


def test_search_comments_no_results():
    post_data = {"image": "post5.png", "text": "Empty search post", "user": "alice"}
    post_id = client.post("/posts/", json=post_data).json()["id"]

    r = client.get(
        f"/posts/{post_id}/comments", params={"text": "nonexistent", "user": "nouser"}
    )
    assert r.status_code == 404
    data = r.json()
    assert data["detail"] == "No comments found for this post"

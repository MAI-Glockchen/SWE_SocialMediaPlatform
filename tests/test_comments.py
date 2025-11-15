import pytest
from fastapi.testclient import TestClient

from app.main import app, init_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()


def create_test_post():
    """Helper: returns ID of a created post"""
    post_data = {"image": "post.png", "text": "parent post", "user": "tester"}
    r = client.post("/posts/", json=post_data)
    return r.json()["id"]


def test_create_comment():
    post_id = create_test_post()

    comment_data = {"text": "nice post!", "user": "alice"}

    r = client.post(f"/posts/{post_id}/comments", json=comment_data)
    assert r.status_code == 200

    data = r.json()
    assert data["user"] == "alice"
    assert data["text"] == "nice post!"
    assert data["super_id"] == post_id
    assert "created_at" in data


def test_get_comments_for_post():
    post_id = create_test_post()

    # create 2 comments
    for user in ["bob", "carol"]:
        client.post(
            f"/posts/{post_id}/comments",
            json={"text": "hi", "user": user},
        )

    r = client.get(f"/posts/{post_id}/comments")
    assert r.status_code == 200

    comments = r.json()
    assert isinstance(comments, list)
    assert len(comments) >= 2

    assert "super_id" in comments[0]
    assert "text" in comments[0]
    assert "user" in comments[0]
    assert "created_at" in comments[0]


def test_get_comments_invalid_post():
    r = client.get("/posts/999999999/comments")
    assert r.status_code == 404

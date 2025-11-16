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


def test_get_comment_by_id():
    post_id = create_test_post()

    # Erstelle einen Kommentar
    comment_data = {"text": "unique comment", "user": "dave"}
    r = client.post(f"/posts/{post_id}/comments", json=comment_data)
    assert r.status_code == 200
    comment_id = r.json()["comment_id"]

    # GET Kommentar nach ID
    r2 = client.get(f"/comments/{comment_id}")
    assert r2.status_code == 200
    data = r2.json()
    assert (
        data["comment_id"] == comment_id
    ), f"Expected comment ID {comment_id}, got {data['id']}"
    assert data["user"] == "dave", f"Expected user 'dave', got {data['user']}"
    assert (
        data["text"] == "unique comment"
    ), f"Expected text 'unique comment', got {data['text']}"

    # Test nicht existierender Kommentar
    r3 = client.get("/comments/999999999")
    assert (
        r3.status_code == 404
    ), f"Expected 404 for non-existent comment, got {r3.status_code}"
    assert r3.json()["detail"] == "Comment not found"

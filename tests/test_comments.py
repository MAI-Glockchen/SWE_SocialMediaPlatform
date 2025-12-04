import base64

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from backend.main import app, get_session_dep

# Use file-based SQLite for tests so tables persist across connections
TEST_DB_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(test_engine)
client = TestClient(app)


def get_test_session():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session_dep] = get_test_session


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(test_engine)


@pytest.fixture(autouse=True)
def clean_db_after_test():
    """Clean all tables using SQLAlchemy ORM after each test"""
    yield
    with Session(test_engine) as session:
        for model in reversed(SQLModel.metadata.sorted_tables):
            session.exec(model.delete())
        session.commit()


# -------------------------
# Helpers
# -------------------------


def encode_image(s: str) -> str:
    """Encode image string to Base64 so the API accepts it."""
    return base64.b64encode(s.encode()).decode()


def create_test_post():
    """Helper: returns ID of a created post"""
    post_data = {
        "image": encode_image("post.png"),
        "text": "parent post",
        "user": "tester",
    }
    r = client.post("/posts/", json=post_data)
    assert r.status_code == 200, r.text
    return r.json()["id"]


# -------------------------
# Tests
# -------------------------


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
        client.post(f"/posts/{post_id}/comments", json={"text": "hi", "user": user})

    r = client.get(f"/posts/{post_id}/comments")
    assert r.status_code == 200

    comments = r.json()
    assert isinstance(comments, list)
    assert len(comments) >= 2

    assert "super_id" in comments[0]
    assert "text" in comments[0]
    assert "user" in comments[0]
    assert "created_at" in comments[0]


def test_get_comment_by_id():
    post_id = create_test_post()

    # Create a comment
    comment_data = {"text": "unique comment", "user": "dave"}
    r = client.post(f"/posts/{post_id}/comments", json=comment_data)
    assert r.status_code == 200
    comment_id = r.json()["comment_id"]

    # GET comment by ID
    r2 = client.get(f"/comments/{comment_id}")
    assert r2.status_code == 200
    data = r2.json()

    assert data["comment_id"] == comment_id
    assert data["user"] == "dave"
    assert data["text"] == "unique comment"

    # GET non-existing comment
    r3 = client.get("/comments/999999999")
    assert r3.status_code == 404
    assert r3.json()["detail"] == "Comment not found"

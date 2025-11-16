import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.main import app, get_session_dep

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
            session.query(model).delete()
        session.commit()


# Helpers
def create_test_post():
    """Helper: returns ID of a created post"""
    post_data = {"image": "post.png", "text": "parent post", "user": "tester"}
    r = client.post("/posts/", json=post_data)
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


def test_get_comments_invalid_post():
    r = client.get("/posts/999999999/comments")
    assert r.status_code == 404

import base64

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from backend.main import app, get_session_dep

# --------------------------
# Setup Test DB
# --------------------------
TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)


def get_test_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session_dep] = get_test_session
client = TestClient(app)


# --------------------------
# Fixtures
# --------------------------
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)


@pytest.fixture(autouse=True)
def clean_db_after_test():
    """Clean DB after each test"""
    yield
    with Session(engine) as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()


# --------------------------
# Helpers
# --------------------------
def encode_image(name: str) -> str:
    """Encode dummy image name into Base64"""
    return base64.b64encode(name.encode()).decode()


def create_post(text="Test post", user="tester", image="myimg.png"):
    payload = {
        "image": encode_image(image),
        "text": text,
        "user": user,
    }
    r = client.post("/posts/", json=payload)
    assert r.status_code == 200, f"Failed to create post: {r.text}"
    return r.json()["id"]


# --------------------------
# Tests
# --------------------------
def test_create_comment_for_post():
    post_id = create_post(text="Post for comments", user="alice", image="post.png")

    comment_data = {"text": "Hello comment", "user": "bob"}
    r = client.post(f"/posts/{post_id}/comments", json=comment_data)

    assert r.status_code == 200
    data = r.json()
    assert data["user"] == "bob"
    assert data["text"] == "Hello comment"


def test_search_comments_by_text():
    post_id = create_post(text="Another post", user="alice", image="p2.png")

    client.post(f"/posts/{post_id}/comments", json={"text": "FindMe123", "user": "bob"})
    client.post(
        f"/posts/{post_id}/comments", json={"text": "Something else", "user": "charlie"}
    )

    r = client.get(f"/posts/{post_id}/comments", params={"text": "FindMe123"})

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["text"] == "FindMe123"


def test_search_comments_by_user():
    post_id = create_post(text="Post X", user="alice", image="p3.png")

    client.post(f"/posts/{post_id}/comments", json={"text": "C1", "user": "u1"})
    client.post(f"/posts/{post_id}/comments", json={"text": "C2", "user": "u1"})
    client.post(f"/posts/{post_id}/comments", json={"text": "C3", "user": "u2"})

    r = client.get(f"/posts/{post_id}/comments", params={"user": "u1"})

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    assert all(c["user"] == "u1" for c in data)


def test_search_comments_by_text_and_user():
    post_id = create_post(text="Combo post", user="alice", image="p4.png")

    client.post(
        f"/posts/{post_id}/comments", json={"text": "UniqueABC", "user": "userA"}
    )
    client.post(
        f"/posts/{post_id}/comments", json={"text": "UniqueABC", "user": "userB"}
    )

    r = client.get(
        f"/posts/{post_id}/comments", params={"text": "UniqueABC", "user": "userA"}
    )

    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["text"] == "UniqueABC"
    assert data[0]["user"] == "userA"


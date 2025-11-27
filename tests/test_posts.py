import base64

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from backend.main import app, get_session_dep

# Test DB
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
    yield
    with Session(engine) as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()


# --------------------------
# Helpers
# --------------------------


def encode_image(name: str) -> str:
    """Encode dummy filename into Base64"""
    return base64.b64encode(name.encode()).decode()


def create_post(image="post.png", text="parent post", user="tester"):
    """Unified post creation helper"""
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


def test_create_post():
    post_data = {
        "image": encode_image("hello.png"),
        "text": "Hello world",
        "user": "alice",
    }

    r = client.post("/posts/", json=post_data)
    assert r.status_code == 200, r.text

    data = r.json()
    assert data["user"] == "alice"
    assert "created_at" in data


def test_get_all_posts():
    create_post()
    create_post()
    create_post()

    r = client.get("/posts/")
    assert r.status_code == 200

    posts = r.json()
    assert isinstance(posts, list)
    assert len(posts) >= 3

    required = {"id", "user", "image", "text", "created_at"}
    for key in required:
        assert key in posts[0]


def test_get_post_by_id():
    post_id = create_post(text="test-text")

    r = client.get(f"/posts/{post_id}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == post_id
    assert data["text"] == "test-text"


def test_get_post_not_found():
    r = client.get("/posts/999999999999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Post not found"


def test_create_multiple_posts_and_get_all():
    for i in range(3):
        create_post(text=f"Post {i}", user=f"user{i}")

    r = client.get("/posts/")
    assert r.status_code == 200

    posts = r.json()
    assert len(posts) >= 3

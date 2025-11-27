import base64

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from backend.main import app, get_session_dep

# --------------------------
# Setup test DB
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


def create_post(text="Test text", user="tester", image="img.png"):
    """Unified helper for creating posts with Base64 images"""
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


def test_search_posts_by_text():
    create_post(text="Search test 123", user="bob", image="dog.png")

    r = client.get("/posts/", params={"text": "Search test 123"})
    assert r.status_code == 200, f"Search request failed: {r.text}"

    data = r.json()
    assert len(data) > 0, "No search results returned"

    for post in data:
        assert "Search" in post["text"]


def test_search_posts_by_user():
    create_post(text="Hello", user="testerA", image="one.png")
    create_post(text="Another", user="testerA", image="two.png")

    r = client.get("/posts/", params={"user": "testerA"})
    assert r.status_code == 200

    data = r.json()
    assert len(data) > 0
    assert all(post["user"] == "testerA" for post in data)


def test_search_posts_by_text_and_user():
    create_post(
        text="UniqueText123456",
        user="unique_user",
        image="img.png",
    )

    r = client.get(
        "/posts/", params={"text": "UniqueText123456", "user": "unique_user"}
    )

    assert r.status_code == 200, r.text
    data = r.json()

    assert len(data) == 1
    assert data[0]["user"] == "unique_user"
    assert "UniqueText123456" in data[0]["text"]


def test_search_no_results():
    r = client.get("/posts/", params={"text": "doesnotexist", "user": "nouser"})
    assert r.status_code == 404
    assert r.json()["detail"] == "No posts found"

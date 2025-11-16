import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.main import app, get_session_dep

# --------------------------
# Setup test database
# --------------------------
TEST_DB_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(test_engine)


def get_test_session():
    with Session(test_engine) as session:
        yield session


# Override dependency
app.dependency_overrides[get_session_dep] = get_test_session

client = TestClient(app)


# --------------------------
# Fixtures
# --------------------------
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(test_engine)


@pytest.fixture(autouse=True)
def clean_db_after_test():
    """Clean all tables after each test"""
    yield
    with Session(test_engine) as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()


# --------------------------
# Helpers
# --------------------------
def create_test_post():
    post_data = {"image": "post.png", "text": "parent post", "user": "tester"}
    r = client.post("/posts/", json=post_data)
    return r.json()["id"]


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
    create_test_post()
    # Search for posts by user "alice"
    r = client.get("/posts/", params={"user": "tester"})
    assert r.status_code == 200
    data = r.json()
    assert all(post["user"] == "tester" for post in data)
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

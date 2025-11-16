import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.main import app, get_session_dep

# Test database setup
TEST_DB_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(test_engine)


# Dependency override
def get_test_session():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session_dep] = get_test_session

# Test client
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(test_engine)


@pytest.fixture(autouse=True)
def clean_db_after_test():
    yield
    with Session(test_engine) as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.query(table).delete()
        session.commit()


# Helpers
def create_test_post():
    post_data = {"image": "post.png", "text": "parent post", "user": "tester"}
    r = client.post("/posts/", json=post_data)
    return r.json()["id"]


# -------------------------
# Tests
# -------------------------
def test_create_post():
    post_data = {"image": "cat.png", "text": "Hello world", "user": "alice"}
    r = client.post("/posts/", json=post_data)
    assert r.status_code == 200
    data = r.json()
    assert data["user"] == "alice"
    assert "created_at" in data


def test_get_all_posts():
    create_test_post()
    r = client.get("/posts/")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Check that all expected keys are there
    required_keys = {"id", "user", "image", "text", "created_at"}
    for key in required_keys:
        assert key in data[0]


def test_get_post_by_id():
    post_id = create_test_post()
    r = client.get(f"/posts/{post_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == post_id
    assert data["text"] == "parent post"


def test_get_post_not_found():
    non_existent_id = 9999991231232351
    r = client.get(f"/posts/{non_existent_id}")
    assert r.status_code == 404
    data = r.json()
    assert data["detail"] == "Post not found"


def test_create_multiple_posts_and_get_all():
    for i in range(3):
        post_data = {"image": f"img{i}.png", "text": f"Post {i}", "user": f"user{i}"}
        client.post("/posts/", json=post_data)

    r = client.get("/posts/")
    data = r.json()
    assert len(data) >= 3

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
            session.exec(table.delete())
        session.commit()


# --------------------------
# Helpers
# --------------------------
def encode_image(s: str) -> str:
    return base64.b64encode(s.encode()).decode()


def create_post(text="Test delete", user="u", image="x.png"):
    payload = {
        "image": encode_image(image),
        "text": text,
        "user": user,
    }
    r = client.post("/posts/", json=payload)
    assert r.status_code == 200
    return r.json()["id"]


def create_comment(post_id, text="comment text", user="u2"):
    payload = {"text": text, "user": user}
    r = client.post(f"/posts/{post_id}/comments", json=payload)
    assert r.status_code == 200
    return r.json()["comment_id"]


# --------------------------
# DELETE Tests
# --------------------------
def test_delete_comment():
    post_id = create_post()
    comment_id = create_comment(post_id)

    # Delete the comment
    r = client.delete(f"/comments/{comment_id}")
    assert r.status_code == 204

    # Comment must no longer exist
    r2 = client.get(f"/comments/{comment_id}")
    assert r2.status_code == 404
    assert r2.json()["detail"] == "Comment not found"


def test_delete_post_and_its_comments():
    post_id = create_post()

    # Create 2 comments
    c1 = create_comment(post_id, text="A")
    c2 = create_comment(post_id, text="B")

    # Delete the post
    r = client.delete(f"/posts/{post_id}")
    assert r.status_code == 204

    # Post should be gone
    r2 = client.get(f"/posts/{post_id}")
    assert r2.status_code == 404
    assert r2.json()["detail"] == "Post not found"

    # Comments should also be gone
    r3 = client.get(f"/comments/{c1}")
    assert r3.status_code == 404

    r4 = client.get(f"/comments/{c2}")
    assert r4.status_code == 404


def test_delete_nonexistent_post():
    r = client.delete("/posts/999999999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Post not found"


def test_delete_nonexistent_comment():
    r = client.delete("/comments/999999999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Comment not found"

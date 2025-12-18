import os
os.environ["WALLOH_SOCIAL_TESTING"] = "1"

import base64
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from backend.main import app, get_session


TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})

# --------------------------
# Dependency override
# --------------------------
def get_test_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)

# --------------------------
# Fixtures
# --------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    SQLModel.metadata.drop_all(engine)
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
def encode_image(content: str) -> str:
    return base64.b64encode(content.encode()).decode()

def create_post(text="Test", user="tester", image="img.png"):
    payload = {
        "image": encode_image(image),
        "text": text,
        "user": user,
    }
    r = client.post("/posts/", json=payload)
    assert r.status_code == 200
    return r.json()["id"]

def create_comment(post_id, text="Test comment", user="tester2"):
    payload = {"text": text, "user": user}
    r = client.post(f"/posts/{post_id}/comments", json=payload)
    assert r.status_code == 200
    return r.json()["comment_id"]

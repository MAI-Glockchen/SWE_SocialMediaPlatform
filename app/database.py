from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "sqlite" / "social.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session():
    with Session(engine) as session:
        yield session

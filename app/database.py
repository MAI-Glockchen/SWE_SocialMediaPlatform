from contextlib import contextmanager
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "sqlite" / "social.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DB_URL = f"sqlite:///{DB_PATH}"
TEST_DB_URL = "sqlite:///:memory:"

engine = create_engine(DB_URL, echo=True)
test_engine = create_engine(TEST_DB_URL, echo=True)


# --------------------------
# Database setup
# --------------------------
def init_db():
    SQLModel.metadata.create_all(engine)


def init_test_db():
    SQLModel.metadata.create_all(test_engine)


# --------------------------
# Session context managers
# --------------------------
@contextmanager
def get_session():
    with Session(engine) as session:
        yield session


@contextmanager
def get_test_session():
    with Session(test_engine) as session:
        yield session


# def reset_prod_db():
#    with Session(engine) as session:
#        for table in reversed(SQLModel.metadata.sorted_tables):
#            session.execute(table.delete())
#        session.commit()

import os
from contextlib import contextmanager
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

# Load .env file
load_dotenv()

# Base project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Env vars
ENV_DB_PATH = os.getenv("DB_PATH")
ENV_DB_URL = os.getenv("DB_URL")
ENV_TEST_DB_URL = os.getenv("TEST_DB_URL", "sqlite:///:memory:")
ENV_DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"

# If DB_PATH is provided, ensure directories exist
if ENV_DB_PATH:
    db_file = Path(ENV_DB_PATH)
    db_file.parent.mkdir(parents=True, exist_ok=True)

# Database URLs
DB_URL = ENV_DB_URL or f"sqlite:///{PROJECT_ROOT / 'sqlite' / 'social.db'}"

engine = create_engine(DB_URL, echo=ENV_DB_ECHO)
test_engine = create_engine(ENV_TEST_DB_URL, echo=False)


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
#            session.exec(table.delete())
#        session.commit()

import os
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session

# 1) Detect if we are running tests
TESTING = os.environ.get("WALLOH_SOCIAL_TESTING") == "1"

if TESTING:
    DATABASE_URL = os.environ.get("TEST_DB_URL", "sqlite:///:memory:")
else:
    DATABASE_URL = os.environ.get("DB_URL", "sqlite:///sqlite/social.db")

# 2) If using a file-based DB, ensure directory exists (but NOT during tests)
if not TESTING and DATABASE_URL.startswith("sqlite") and "memory" not in DATABASE_URL:
    db_path = DATABASE_URL.replace("sqlite:///", "")
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

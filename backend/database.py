from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

SQLALCHEMY_DATABASE_URL = "sqlite:///./litgraph.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def commit_or_rollback(db):
    """
    Commit if possible. If the DB throws IntegrityError, rollback and re-raise.
    """
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

def handle_integrity_error(e: IntegrityError):
    msg = str(e.orig).lower()

    # uniqueness
    if "unique" in msg or "uq_" in msg:
        return HTTPException(status_code=409, detail="Already exists")

    # foreign key
    if "foreign key" in msg:
        return HTTPException(status_code=400, detail="Invalid foreign key reference")

    # not null
    if "not null" in msg:
        return HTTPException(status_code=400, detail="Missing required field")

    return HTTPException(status_code=400, detail="Database constraint error")
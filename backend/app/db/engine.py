from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker
import os
from app.core.config import settings


DATABASE_URL = settings.SUPABASE_DB_URL

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

def init_db():
    SQLModel.metadata.create_all(engine)

SessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
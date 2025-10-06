"""
Database connection and session management
"""
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
import os
from pathlib import Path

# Uygulama veri dizini
DATA_DIR = Path(os.getenv("APPDATA", ".")) / "lab-report-app"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# SQLite veritabanı yolu
DATABASE_URL = f"sqlite:///{DATA_DIR / 'lab_reports.db'}"

# Engine oluştur
engine = create_engine(
    DATABASE_URL,
    echo=False,  # SQL sorgularını logla (geliştirme için True)
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def create_db_and_tables():
    """Veritabanı ve tabloları oluştur"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Veritabanı session'ı döndür (dependency injection için)"""
    with Session(engine) as session:
        yield session

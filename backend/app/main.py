"""
FastAPI main application
Lab Report Management System - MVP Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pathlib import Path

from app.database import create_db_and_tables
from app.api import projects, experiments, entries, attachments, datasets, reports, search, templates


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama başlangıç ve kapanış olayları"""
    # Başlangıç: Veritabanını oluştur
    create_db_and_tables()
    print("✅ Database initialized")
    yield
    # Kapanış: Temizlik işlemleri
    print("👋 Application shutdown")


app = FastAPI(
    title="Lab Report Management API",
    description="Laboratuvar rapor yönetim sistemi - Offline-first backend",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware (sadece localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",  # Frontend aynı porttan sunulacak
        "http://127.0.0.1:8000",
        "http://localhost:5173",  # Vite dev server (gelecek için)
        "http://127.0.0.1:5173",
        "tauri://localhost",      # Tauri
        "http://tauri.localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API router'ları dahil et
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(experiments.router, prefix="/api/experiments", tags=["Experiments"])
app.include_router(entries.router, prefix="/api/entries", tags=["Entries"])
app.include_router(attachments.router, prefix="/api/attachments", tags=["Attachments"])
app.include_router(datasets.router, prefix="/api/datasets", tags=["Datasets"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(templates.router, prefix="/api/templates", tags=["Templates"])

# Frontend klasörünü belirle
FRONTEND_DIR = Path(__file__).parent.parent.parent / "frontend"

# Frontend için root endpoint
@app.get("/")
async def serve_frontend():
    """Ana sayfa - Frontend HTML'i göster"""
    html_path = FRONTEND_DIR / "index.html"
    if html_path.exists():
        return FileResponse(html_path)
    return {
        "status": "running",
        "app": "Lab Report Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "message": "Frontend not found. Please create frontend/index.html"
    }


@app.get("/health")
async def health_check():
    """Sağlık kontrolü"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
    )

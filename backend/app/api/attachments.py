"""
Attachments API - dosya yükleme ve yönetimi
"""
import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from app.database import get_session, DATA_DIR
from app.models import Attachment, Entry, AuditLog
from app.schemas import AttachmentRead

router = APIRouter()

# Desteklenen dosya tipleri ve maksimum boyutlar
ALLOWED_EXTENSIONS = {
    "png": 10 * 1024 * 1024,   # 10MB
    "jpg": 10 * 1024 * 1024,   # 10MB
    "jpeg": 10 * 1024 * 1024,  # 10MB
    "pdf": 20 * 1024 * 1024,   # 20MB
    "docx": 20 * 1024 * 1024,  # 20MB
    "xlsx": 20 * 1024 * 1024,  # 20MB
    "csv": 10 * 1024 * 1024,   # 10MB
}

# Storage dizini
STORAGE_DIR = DATA_DIR / "storage" / "attachments"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def get_file_hash(content: bytes) -> str:
    """Dosya SHA256 hash'ini hesapla"""
    return hashlib.sha256(content).hexdigest()


def get_file_extension(filename: str) -> str:
    """Dosya uzantısını al"""
    return filename.lower().split(".")[-1] if "." in filename else ""


def validate_file(file: UploadFile, content: bytes) -> tuple[bool, str]:
    """Dosya validasyonu"""
    ext = get_file_extension(file.filename)
    
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Desteklenmeyen dosya tipi: {ext}. İzin verilenler: {', '.join(ALLOWED_EXTENSIONS.keys())}"
    
    max_size = ALLOWED_EXTENSIONS[ext]
    if len(content) > max_size:
        return False, f"Dosya çok büyük. Maksimum boyut: {max_size / (1024*1024):.1f}MB"
    
    return True, ""


@router.post("/", response_model=AttachmentRead, status_code=201)
async def upload_attachment(
    entry_id: int = Query(..., description="Bağlı olduğu entry ID"),
    caption: Optional[str] = Query(None, description="Dosya açıklaması"),
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    """Dosya yükle ve entry'ye bağla"""
    
    # Entry kontrolü
    entry = session.get(Entry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    # Dosyayı oku
    content = await file.read()
    
    # Validasyon
    is_valid, error_msg = validate_file(file, content)
    if not is_valid:
        raise HTTPException(status_code=422, detail=error_msg)
    
    # Hash hesapla
    file_hash = get_file_hash(content)
    
    # Aynı dosya daha önce yüklendi mi?
    existing = session.exec(
        select(Attachment).where(Attachment.sha256 == file_hash)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Bu dosya zaten yüklendi (ID: {existing.id})"
        )
    
    # Storage yolu oluştur: storage/attachments/yyyy/mm/hash.ext
    now = datetime.utcnow()
    year_dir = STORAGE_DIR / str(now.year)
    month_dir = year_dir / f"{now.month:02d}"
    month_dir.mkdir(parents=True, exist_ok=True)
    
    ext = get_file_extension(file.filename)
    file_path = month_dir / f"{file_hash[:16]}.{ext}"
    
    # Dosyayı kaydet
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Veritabanına kaydet (relative path)
    relative_path = str(file_path.relative_to(DATA_DIR))
    
    db_attachment = Attachment(
        entry_id=entry_id,
        file_path=relative_path,
        file_type=ext,
        file_size=len(content),
        original_name=file.filename,
        caption=caption,
        sha256=file_hash,
    )
    
    session.add(db_attachment)
    session.commit()
    session.refresh(db_attachment)
    
    # Audit log
    audit = AuditLog(
        entity="attachment",
        entity_id=db_attachment.id,
        who=entry.author_id,
        action="create",
    )
    session.add(audit)
    session.commit()
    
    return db_attachment


@router.get("/", response_model=List[AttachmentRead])
async def list_attachments(
    entry_id: Optional[int] = Query(None),
    file_type: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    """Dosyaları listele"""
    statement = select(Attachment)
    
    if entry_id:
        statement = statement.where(Attachment.entry_id == entry_id)
    
    if file_type:
        statement = statement.where(Attachment.file_type == file_type)
    
    statement = statement.order_by(Attachment.created_at.desc()).offset(offset).limit(limit)
    attachments = session.exec(statement).all()
    
    return attachments


@router.get("/{attachment_id}", response_model=AttachmentRead)
async def get_attachment(
    attachment_id: int,
    session: Session = Depends(get_session),
):
    """Dosya detayı"""
    attachment = session.get(Attachment, attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return attachment


@router.get("/{attachment_id}/download")
async def download_attachment(
    attachment_id: int,
    session: Session = Depends(get_session),
):
    """Dosyayı indir"""
    attachment = session.get(Attachment, attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    file_path = DATA_DIR / attachment.file_path
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=attachment.original_name,
        media_type=f"application/{attachment.file_type}",
    )


@router.delete("/{attachment_id}")
async def delete_attachment(
    attachment_id: int,
    user_id: int = Query(..., description="İşlemi yapan kullanıcı ID"),
    session: Session = Depends(get_session),
):
    """Dosyayı sil"""
    attachment = session.get(Attachment, attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    # Dosyayı diskten sil
    file_path = DATA_DIR / attachment.file_path
    if file_path.exists():
        file_path.unlink()
    
    # Audit log
    audit = AuditLog(
        entity="attachment",
        entity_id=attachment_id,
        who=user_id,
        action="delete",
    )
    session.add(audit)
    
    # Veritabanından sil
    session.delete(attachment)
    session.commit()
    
    return {"status": "deleted", "attachment_id": attachment_id}

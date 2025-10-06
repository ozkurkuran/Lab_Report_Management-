"""
Entries API endpoints
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models import Entry, AuditLog
from app.schemas import EntryCreate, EntryUpdate, EntryRead

router = APIRouter()


@router.post("/", response_model=EntryRead, status_code=201)
async def create_entry(
    entry: EntryCreate,
    session: Session = Depends(get_session),
):
    """Yeni entry oluştur"""
    db_entry = Entry(**entry.model_dump())
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    
    # Audit log
    audit = AuditLog(
        entity="entry",
        entity_id=db_entry.id,
        who=entry.author_id,
        action="create",
    )
    session.add(audit)
    session.commit()
    
    return db_entry


@router.patch("/{entry_id}", response_model=EntryRead)
async def update_entry(
    entry_id: int,
    entry_update: EntryUpdate,
    session: Session = Depends(get_session),
):
    """Entry güncelle (yeni versiyon oluştur)"""
    # Mevcut entry'yi bul
    old_entry = session.get(Entry, entry_id)
    if not old_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    # Yeni versiyon oluştur
    new_entry_data = old_entry.model_dump()
    new_entry_data.pop("id")
    new_entry_data["version"] = old_entry.version + 1
    new_entry_data["parent_version_id"] = entry_id
    new_entry_data["updated_at"] = datetime.utcnow()
    
    # Güncellenen alanları uygula
    update_data = entry_update.model_dump(exclude_unset=True)
    new_entry_data.update(update_data)
    
    # Yeni entry kaydet
    db_entry = Entry(**new_entry_data)
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    
    # Audit log
    audit = AuditLog(
        entity="entry",
        entity_id=db_entry.id,
        who=old_entry.author_id,
        action="update",
        diff_json=update_data,
    )
    session.add(audit)
    session.commit()
    
    return db_entry


@router.get("/", response_model=List[EntryRead])
async def list_entries(
    experiment_id: Optional[int] = Query(None),
    author_id: Optional[int] = Query(None),
    tag: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    """Entry'leri listele"""
    statement = select(Entry)
    
    if experiment_id:
        statement = statement.where(Entry.experiment_id == experiment_id)
    
    if author_id:
        statement = statement.where(Entry.author_id == author_id)
    
    if tag:
        statement = statement.where(Entry.tags.contains(tag))
    
    if date_from:
        statement = statement.where(Entry.created_at >= date_from)
    
    if date_to:
        statement = statement.where(Entry.created_at <= date_to)
    
    statement = statement.order_by(Entry.created_at.desc()).offset(offset).limit(limit)
    entries = session.exec(statement).all()
    
    return entries


@router.get("/{entry_id}", response_model=EntryRead)
async def get_entry(
    entry_id: int,
    session: Session = Depends(get_session),
):
    """Entry detayı"""
    entry = session.get(Entry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.get("/{entry_id}/versions", response_model=List[EntryRead])
async def get_entry_versions(
    entry_id: int,
    session: Session = Depends(get_session),
):
    """Entry'nin tüm versiyonlarını getir"""
    # İlk versiyonu bul
    entry = session.get(Entry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    # Tüm versiyonları bul
    statement = select(Entry).where(
        (Entry.id == entry_id) | (Entry.parent_version_id == entry_id)
    ).order_by(Entry.version)
    
    versions = session.exec(statement).all()
    return versions

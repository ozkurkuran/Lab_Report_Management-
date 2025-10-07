"""
Search API - çoklu kriter arama
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, or_, and_

from app.database import get_session
from app.models import Entry, Experiment, Project
from app.schemas import EntryRead, ExperimentRead, ProjectRead

router = APIRouter()


@router.get("/entries", response_model=List[EntryRead])
async def search_entries(
    text: Optional[str] = Query(None, description="Başlık veya içerikte ara"),
    project_id: Optional[int] = Query(None),
    experiment_id: Optional[int] = Query(None),
    tags: Optional[str] = Query(None, description="Virgülle ayrılmış etiketler"),
    author_id: Optional[int] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    """Entry'lerde arama yap"""
    
    statement = select(Entry)
    
    # Metin araması (başlık veya içerik)
    if text:
        statement = statement.where(
            or_(
                Entry.title.contains(text),
                Entry.body_md.contains(text)
            )
        )
    
    # Experiment filtresi
    if experiment_id:
        statement = statement.where(Entry.experiment_id == experiment_id)
    elif project_id:
        # Projeye bağlı deneyleri bul
        exp_statement = select(Experiment.id).where(Experiment.project_id == project_id)
        exp_ids = session.exec(exp_statement).all()
        if exp_ids:
            statement = statement.where(Entry.experiment_id.in_(exp_ids))
    
    # Yazar filtresi
    if author_id:
        statement = statement.where(Entry.author_id == author_id)
    
    # Tarih aralığı
    if date_from:
        statement = statement.where(Entry.created_at >= date_from)
    if date_to:
        statement = statement.where(Entry.created_at <= date_to)
    
    # Tag filtresi
    if tags:
        tag_list = [t.strip() for t in tags.split(',')]
        for tag in tag_list:
            statement = statement.where(Entry.tags.contains(tag))
    
    statement = statement.order_by(Entry.created_at.desc()).offset(offset).limit(limit)
    entries = session.exec(statement).all()
    
    return entries


@router.get("/experiments", response_model=List[ExperimentRead])
async def search_experiments(
    text: Optional[str] = Query(None, description="Başlık veya açıklamada ara"),
    project_id: Optional[int] = Query(None),
    tags: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
    session: Session = Depends(get_session),
):
    """Deneylerde arama yap"""
    
    statement = select(Experiment)
    
    if text:
        statement = statement.where(
            or_(
                Experiment.title.contains(text),
                Experiment.description.contains(text)
            )
        )
    
    if project_id:
        statement = statement.where(Experiment.project_id == project_id)
    
    if tags:
        tag_list = [t.strip() for t in tags.split(',')]
        for tag in tag_list:
            statement = statement.where(Experiment.tags.contains(tag))
    
    statement = statement.order_by(Experiment.start_ts.desc()).limit(limit)
    experiments = session.exec(statement).all()
    
    return experiments


@router.get("/projects", response_model=List[ProjectRead])
async def search_projects(
    text: Optional[str] = Query(None, description="Proje adında ara"),
    tags: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
    session: Session = Depends(get_session),
):
    """Projelerde arama yap"""
    
    statement = select(Project)
    
    if text:
        statement = statement.where(
            or_(
                Project.name.contains(text),
                Project.description.contains(text)
            )
        )
    
    if tags:
        tag_list = [t.strip() for t in tags.split(',')]
        for tag in tag_list:
            statement = statement.where(Project.tags.contains(tag))
    
    statement = statement.order_by(Project.created_at.desc()).limit(limit)
    projects = session.exec(statement).all()
    
    return projects


@router.get("/all")
async def search_all(
    text: str = Query(..., min_length=2, description="Arama metni"),
    limit: int = Query(20, le=100),
    session: Session = Depends(get_session),
):
    """Tüm entity'lerde arama yap (birleşik sonuç)"""
    
    # Projects
    proj_statement = select(Project).where(
        or_(
            Project.name.contains(text),
            Project.description.contains(text)
        )
    ).limit(limit)
    projects = session.exec(proj_statement).all()
    
    # Experiments
    exp_statement = select(Experiment).where(
        or_(
            Experiment.title.contains(text),
            Experiment.description.contains(text)
        )
    ).limit(limit)
    experiments = session.exec(exp_statement).all()
    
    # Entries
    entry_statement = select(Entry).where(
        or_(
            Entry.title.contains(text),
            Entry.body_md.contains(text)
        )
    ).limit(limit)
    entries = session.exec(entry_statement).all()
    
    return {
        "query": text,
        "results": {
            "projects": [{"id": p.id, "name": p.name, "type": "project"} for p in projects],
            "experiments": [{"id": e.id, "title": e.title, "type": "experiment"} for e in experiments],
            "entries": [{"id": e.id, "title": e.title, "type": "entry"} for e in entries],
        },
        "total": len(projects) + len(experiments) + len(entries)
    }

"""
Projects API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models import Project, AuditLog
from app.schemas import ProjectCreate, ProjectRead

router = APIRouter()


@router.post("/", response_model=ProjectRead, status_code=201)
async def create_project(
    project: ProjectCreate,
    session: Session = Depends(get_session),
):
    """Yeni proje oluştur"""
    db_project = Project(**project.model_dump())
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    
    # Audit log
    audit = AuditLog(
        entity="project",
        entity_id=db_project.id,
        who=project.created_by,
        action="create",
    )
    session.add(audit)
    session.commit()
    
    return db_project


@router.get("/", response_model=List[ProjectRead])
async def list_projects(
    query: Optional[str] = Query(None, description="Proje adında arama"),
    tag: Optional[str] = Query(None, description="Etiket filtresi"),
    archived: bool = Query(False, description="Arşivlenmiş projeleri göster"),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    """Projeleri listele"""
    statement = select(Project).where(Project.archived == archived)
    
    if query:
        statement = statement.where(Project.name.contains(query))
    
    if tag:
        # JSON içinde etiket arama (SQLite için basit yaklaşım)
        statement = statement.where(Project.tags.contains(tag))
    
    statement = statement.offset(offset).limit(limit)
    projects = session.exec(statement).all()
    
    return projects


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: int,
    session: Session = Depends(get_session),
):
    """Proje detayı"""
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}/archive")
async def archive_project(
    project_id: int,
    user_id: int = Query(..., description="İşlemi yapan kullanıcı ID"),
    session: Session = Depends(get_session),
):
    """Projeyi arşivle"""
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.archived = True
    session.add(project)
    
    # Audit log
    audit = AuditLog(
        entity="project",
        entity_id=project_id,
        who=user_id,
        action="archive",
    )
    session.add(audit)
    session.commit()
    
    return {"status": "archived", "project_id": project_id}

"""
Experiments API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models import Experiment, AuditLog
from app.schemas import ExperimentCreate, ExperimentRead

router = APIRouter()


@router.post("/", response_model=ExperimentRead, status_code=201)
async def create_experiment(
    experiment: ExperimentCreate,
    user_id: int = Query(..., description="İşlemi yapan kullanıcı ID"),
    session: Session = Depends(get_session),
):
    """Yeni deney oluştur"""
    db_experiment = Experiment(**experiment.model_dump())
    session.add(db_experiment)
    session.commit()
    session.refresh(db_experiment)
    
    # Audit log
    audit = AuditLog(
        entity="experiment",
        entity_id=db_experiment.id,
        who=user_id,
        action="create",
    )
    session.add(audit)
    session.commit()
    
    return db_experiment


@router.get("/", response_model=List[ExperimentRead])
async def list_experiments(
    project_id: Optional[int] = Query(None),
    tag: Optional[str] = Query(None),
    archived: bool = Query(False),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    """Deneyleri listele"""
    statement = select(Experiment).where(Experiment.archived == archived)
    
    if project_id:
        statement = statement.where(Experiment.project_id == project_id)
    
    if tag:
        statement = statement.where(Experiment.tags.contains(tag))
    
    statement = statement.offset(offset).limit(limit)
    experiments = session.exec(statement).all()
    
    return experiments


@router.get("/{experiment_id}", response_model=ExperimentRead)
async def get_experiment(
    experiment_id: int,
    session: Session = Depends(get_session),
):
    """Deney detayı"""
    experiment = session.get(Experiment, experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment

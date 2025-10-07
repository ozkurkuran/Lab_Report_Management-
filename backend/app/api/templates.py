"""
Templates API - rapor şablonu yönetimi
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlmodel import Session, select

from app.database import get_session, DATA_DIR
from app.models import Template
from app.schemas import TemplateRead, TemplateCreate

router = APIRouter()

# Template dizini
TEMPLATE_DIR = DATA_DIR / "templates"
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/", response_model=List[TemplateRead])
async def list_templates(
    type: str = Query(None, description="Şablon tipi: docx, html, pdf"),
    session: Session = Depends(get_session),
):
    """Şablonları listele"""
    statement = select(Template)
    
    if type:
        statement = statement.where(Template.type == type)
    
    statement = statement.order_by(Template.is_default.desc(), Template.created_at.desc())
    templates = session.exec(statement).all()
    
    return templates


@router.get("/{template_id}", response_model=TemplateRead)
async def get_template(
    template_id: int,
    session: Session = Depends(get_session),
):
    """Şablon detayı"""
    template = session.get(Template, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.post("/", response_model=TemplateRead, status_code=201)
async def create_template(
    name: str = Query(...),
    description: str = Query(None),
    type: str = Query(..., pattern="^(docx|html|pdf)$"),
    is_default: bool = Query(False),
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    """Yeni şablon oluştur"""
    
    # Dosyayı kaydet
    content = await file.read()
    file_path = TEMPLATE_DIR / file.filename
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Veritabanına kaydet
    relative_path = str(file_path.relative_to(DATA_DIR))
    
    # Eğer default olarak işaretlendiyse, diğerlerini default'tan çıkar
    if is_default:
        existing_defaults = session.exec(
            select(Template).where(Template.type == type, Template.is_default == True)
        ).all()
        for tpl in existing_defaults:
            tpl.is_default = False
            session.add(tpl)
    
    db_template = Template(
        type=type,
        name=name,
        description=description,
        file_path=relative_path,
        is_default=is_default,
    )
    
    session.add(db_template)
    session.commit()
    session.refresh(db_template)
    
    return db_template


@router.delete("/{template_id}")
async def delete_template(
    template_id: int,
    session: Session = Depends(get_session),
):
    """Şablonu sil"""
    template = session.get(Template, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Dosyayı sil
    try:
        file_path = DATA_DIR / template.file_path
        if file_path.exists():
            file_path.unlink()
    except Exception:
        pass
    
    session.delete(template)
    session.commit()
    
    return {"status": "deleted", "template_id": template_id}

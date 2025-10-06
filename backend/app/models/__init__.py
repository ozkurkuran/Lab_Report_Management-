"""
Database models for Lab Report Management System
"""
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, Column, JSON
from pydantic import EmailStr


class User(SQLModel, table=True):
    """Kullanıcı modeli"""
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: EmailStr = Field(unique=True, index=True)
    role: str = Field(default="researcher")  # researcher, admin, reviewer
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # İlişkiler
    projects: List["Project"] = Relationship(back_populates="creator")
    entries: List["Entry"] = Relationship(back_populates="author")


class Project(SQLModel, table=True):
    """Proje modeli"""
    __tablename__ = "projects"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    created_by: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    archived: bool = Field(default=False)
    
    # İlişkiler
    creator: Optional[User] = Relationship(back_populates="projects")
    experiments: List["Experiment"] = Relationship(back_populates="project")


class Experiment(SQLModel, table=True):
    """Deney modeli"""
    __tablename__ = "experiments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", index=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    start_ts: datetime = Field(default_factory=datetime.utcnow)
    end_ts: Optional[datetime] = None
    archived: bool = Field(default=False)
    
    # İlişkiler
    project: Optional[Project] = Relationship(back_populates="experiments")
    entries: List["Entry"] = Relationship(back_populates="experiment")


class Entry(SQLModel, table=True):
    """Deney günlüğü girişi (versiyonlu)"""
    __tablename__ = "entries"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    experiment_id: int = Field(foreign_key="experiments.id", index=True)
    author_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(index=True)
    body_md: str  # Markdown formatında içerik
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    version: int = Field(default=1)
    parent_version_id: Optional[int] = Field(default=None, foreign_key="entries.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # İlişkiler
    experiment: Optional[Experiment] = Relationship(back_populates="entries")
    author: Optional[User] = Relationship(back_populates="entries")
    attachments: List["Attachment"] = Relationship(back_populates="entry")
    datasets: List["Dataset"] = Relationship(back_populates="entry")


class Attachment(SQLModel, table=True):
    """Dosya eki modeli"""
    __tablename__ = "attachments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    entry_id: int = Field(foreign_key="entries.id", index=True)
    file_path: str  # storage/attachments/yyyy/mm/uuid.ext
    file_type: str  # png, jpg, pdf, docx, xlsx, csv
    file_size: int  # bytes
    original_name: str
    caption: Optional[str] = None
    sha256: str = Field(index=True)  # Dosya hash'i
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # İlişkiler
    entry: Optional[Entry] = Relationship(back_populates="attachments")


class Dataset(SQLModel, table=True):
    """İçe aktarılan veri seti modeli"""
    __tablename__ = "datasets"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    entry_id: int = Field(foreign_key="entries.id", index=True)
    name: str
    source_file: str  # Orijinal dosya yolu
    columns_json: dict = Field(sa_column=Column(JSON))  # Kolon adları ve tipleri
    stats_json: dict = Field(sa_column=Column(JSON))  # İstatistikler (mean, std, vb.)
    row_count: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # İlişkiler
    entry: Optional[Entry] = Relationship(back_populates="datasets")
    charts: List["Chart"] = Relationship(back_populates="dataset")


class Chart(SQLModel, table=True):
    """Üretilen grafik modeli"""
    __tablename__ = "charts"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    dataset_id: int = Field(foreign_key="datasets.id", index=True)
    chart_type: str  # line, scatter, bar, histogram
    x_column: str
    y_column: str
    title: Optional[str] = None
    image_path: str  # PNG dosya yolu
    config_json: dict = Field(sa_column=Column(JSON))  # Grafik ayarları
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # İlişkiler
    dataset: Optional[Dataset] = Relationship(back_populates="charts")


class AuditLog(SQLModel, table=True):
    """Değişiklik kaydı"""
    __tablename__ = "audit_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    entity: str = Field(index=True)  # project, experiment, entry
    entity_id: int = Field(index=True)
    who: int = Field(foreign_key="users.id")  # Kullanıcı ID
    action: str  # create, update, archive
    diff_json: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    ts: datetime = Field(default_factory=datetime.utcnow, index=True)


class Template(SQLModel, table=True):
    """Rapor şablonu modeli"""
    __tablename__ = "templates"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str = Field(index=True)  # docx, html, pdf
    name: str
    description: Optional[str] = None
    file_path: str  # templates/ altında
    is_default: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

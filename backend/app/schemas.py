"""
Pydantic schemas for API request/response validation
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ========== User Schemas ==========
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "researcher"


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Project Schemas ==========
class ProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class ProjectCreate(ProjectBase):
    created_by: int


class ProjectRead(ProjectBase):
    id: int
    created_by: int
    created_at: datetime
    archived: bool
    
    class Config:
        from_attributes = True


# ========== Experiment Schemas ==========
class ExperimentBase(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class ExperimentCreate(ExperimentBase):
    project_id: int


class ExperimentRead(ExperimentBase):
    id: int
    project_id: int
    start_ts: datetime
    end_ts: Optional[datetime] = None
    archived: bool
    
    class Config:
        from_attributes = True


# ========== Entry Schemas ==========
class EntryBase(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    body_md: str
    tags: List[str] = Field(default_factory=list)


class EntryCreate(EntryBase):
    experiment_id: int
    author_id: int


class EntryUpdate(BaseModel):
    title: Optional[str] = None
    body_md: Optional[str] = None
    tags: Optional[List[str]] = None


class EntryRead(EntryBase):
    id: int
    experiment_id: int
    author_id: int
    version: int
    parent_version_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ========== Attachment Schemas ==========
class AttachmentBase(BaseModel):
    caption: Optional[str] = None


class AttachmentRead(AttachmentBase):
    id: int
    entry_id: int
    file_path: str
    file_type: str
    file_size: int
    original_name: str
    sha256: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Dataset Schemas ==========
class DatasetImportRequest(BaseModel):
    entry_id: int
    name: str
    file_type: str  # csv, xlsx


class DatasetRead(BaseModel):
    id: int
    entry_id: int
    name: str
    source_file: str
    columns_json: dict
    stats_json: dict
    row_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Chart Schemas ==========
class ChartCreateRequest(BaseModel):
    dataset_id: int
    chart_type: str = Field(pattern="^(line|scatter|bar|histogram)$")
    x_column: str
    y_column: str
    title: Optional[str] = None
    config_json: dict = Field(default_factory=dict)


class ChartRead(BaseModel):
    id: int
    dataset_id: int
    chart_type: str
    x_column: str
    y_column: str
    title: Optional[str] = None
    image_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Report Schemas ==========
class ReportDOCXRequest(BaseModel):
    entry_id: int
    template_id: int


class ReportPDFRequest(BaseModel):
    entry_id: int
    template_id: Optional[int] = None


class ReportXLSXRequest(BaseModel):
    entry_id: int


# ========== Template Schemas ==========
class TemplateBase(BaseModel):
    type: str = Field(pattern="^(docx|html|pdf)$")
    name: str
    description: Optional[str] = None
    is_default: bool = False


class TemplateCreate(TemplateBase):
    pass


class TemplateRead(TemplateBase):
    id: int
    file_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Search/Filter Schemas ==========
class SearchQuery(BaseModel):
    text: Optional[str] = None
    project_id: Optional[int] = None
    experiment_id: Optional[int] = None
    tags: Optional[List[str]] = None
    author_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    limit: int = Field(default=50, le=200)
    offset: int = Field(default=0, ge=0)


# ========== Audit Log Schemas ==========
class AuditLogRead(BaseModel):
    id: int
    entity: str
    entity_id: int
    who: int
    action: str
    diff_json: Optional[dict] = None
    ts: datetime
    
    class Config:
        from_attributes = True

"""
Datasets API - CSV/XLSX içe aktarma ve grafik üretimi
"""
import io
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlmodel import Session, select
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # GUI olmadan çalışma
import matplotlib.pyplot as plt

from app.database import get_session, DATA_DIR
from app.models import Dataset, Chart, Entry, AuditLog
from app.schemas import DatasetRead, ChartCreateRequest, ChartRead

router = APIRouter()

# Storage dizinleri
DATASET_DIR = DATA_DIR / "storage" / "datasets"
CHART_DIR = DATA_DIR / "storage" / "charts"
DATASET_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/import", response_model=DatasetRead, status_code=201)
async def import_dataset(
    entry_id: int = Query(...),
    name: str = Query(..., description="Dataset adı"),
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    """CSV veya XLSX dosyasını içe aktar"""
    
    # Entry kontrolü
    entry = session.get(Entry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    # Dosya tipini kontrol et
    filename = file.filename.lower()
    if not (filename.endswith('.csv') or filename.endswith('.xlsx')):
        raise HTTPException(
            status_code=422,
            detail="Sadece CSV ve XLSX dosyaları desteklenir"
        )
    
    # Dosyayı oku
    content = await file.read()
    
    # Pandas ile parse et
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Dosya parse hatası: {str(e)}"
        )
    
    if df.empty:
        raise HTTPException(status_code=422, detail="Dosya boş")
    
    # Dosyayı kaydet
    now = datetime.utcnow()
    year_dir = DATASET_DIR / str(now.year)
    month_dir = year_dir / f"{now.month:02d}"
    month_dir.mkdir(parents=True, exist_ok=True)
    
    file_ext = "csv" if filename.endswith('.csv') else "xlsx"
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    file_path = month_dir / f"{name.replace(' ', '_')}_{timestamp}.{file_ext}"
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Kolon bilgileri
    columns_info = {}
    for col in df.columns:
        dtype = str(df[col].dtype)
        columns_info[col] = {
            "dtype": dtype,
            "non_null": int(df[col].count()),
            "unique": int(df[col].nunique())
        }
    
    # İstatistikler (sadece numerik kolonlar)
    stats_info = {}
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        stats_df = df[numeric_cols].describe()
        for col in numeric_cols:
            stats_info[col] = {
                "mean": float(stats_df.loc['mean', col]) if 'mean' in stats_df.index else None,
                "std": float(stats_df.loc['std', col]) if 'std' in stats_df.index else None,
                "min": float(stats_df.loc['min', col]) if 'min' in stats_df.index else None,
                "max": float(stats_df.loc['max', col]) if 'max' in stats_df.index else None,
            }
    
    # Veritabanına kaydet
    relative_path = str(file_path.relative_to(DATA_DIR))
    
    db_dataset = Dataset(
        entry_id=entry_id,
        name=name,
        source_file=relative_path,
        columns_json=columns_info,
        stats_json=stats_info,
        row_count=len(df),
    )
    
    session.add(db_dataset)
    session.commit()
    session.refresh(db_dataset)
    
    # Audit log
    audit = AuditLog(
        entity="dataset",
        entity_id=db_dataset.id,
        who=entry.author_id,
        action="create",
    )
    session.add(audit)
    session.commit()
    
    return db_dataset


@router.get("/", response_model=List[DatasetRead])
async def list_datasets(
    entry_id: Optional[int] = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    """Dataset'leri listele"""
    statement = select(Dataset)
    
    if entry_id:
        statement = statement.where(Dataset.entry_id == entry_id)
    
    statement = statement.order_by(Dataset.created_at.desc()).offset(offset).limit(limit)
    datasets = session.exec(statement).all()
    
    return datasets


@router.get("/{dataset_id}", response_model=DatasetRead)
async def get_dataset(
    dataset_id: int,
    session: Session = Depends(get_session),
):
    """Dataset detayı"""
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset


@router.get("/{dataset_id}/preview")
async def preview_dataset(
    dataset_id: int,
    rows: int = Query(100, le=1000, description="Gösterilecek satır sayısı"),
    session: Session = Depends(get_session),
):
    """Dataset önizlemesi (ilk N satır)"""
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    file_path = DATA_DIR / dataset.source_file
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Source file not found")
    
    # Dosyayı oku
    try:
        if dataset.source_file.endswith('.csv'):
            df = pd.read_csv(file_path, nrows=rows)
        else:
            df = pd.read_excel(file_path, nrows=rows)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Read error: {str(e)}")
    
    return {
        "dataset_id": dataset_id,
        "name": dataset.name,
        "total_rows": dataset.row_count,
        "preview_rows": len(df),
        "columns": list(df.columns),
        "data": df.to_dict(orient='records')
    }


@router.post("/{dataset_id}/chart", response_model=ChartRead, status_code=201)
async def create_chart(
    dataset_id: int,
    chart_request: ChartCreateRequest,
    user_id: int = Query(..., description="İşlemi yapan kullanıcı ID"),
    session: Session = Depends(get_session),
):
    """Dataset'ten grafik üret"""
    
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Dosyayı oku
    file_path = DATA_DIR / dataset.source_file
    try:
        if dataset.source_file.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Read error: {str(e)}")
    
    # Kolon kontrolü
    if chart_request.x_column not in df.columns:
        raise HTTPException(status_code=422, detail=f"Column '{chart_request.x_column}' not found")
    if chart_request.y_column not in df.columns:
        raise HTTPException(status_code=422, detail=f"Column '{chart_request.y_column}' not found")
    
    # Grafik oluştur
    plt.figure(figsize=(10, 6))
    
    if chart_request.chart_type == "line":
        plt.plot(df[chart_request.x_column], df[chart_request.y_column], marker='o')
    elif chart_request.chart_type == "scatter":
        plt.scatter(df[chart_request.x_column], df[chart_request.y_column])
    elif chart_request.chart_type == "bar":
        plt.bar(df[chart_request.x_column], df[chart_request.y_column])
    elif chart_request.chart_type == "histogram":
        plt.hist(df[chart_request.y_column], bins=30)
    else:
        raise HTTPException(status_code=422, detail="Invalid chart type")
    
    plt.xlabel(chart_request.x_column)
    plt.ylabel(chart_request.y_column)
    plt.title(chart_request.title or f"{chart_request.y_column} vs {chart_request.x_column}")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Grafiği kaydet
    now = datetime.utcnow()
    year_dir = CHART_DIR / str(now.year)
    month_dir = year_dir / f"{now.month:02d}"
    month_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    chart_filename = f"chart_{dataset_id}_{timestamp}.png"
    chart_path = month_dir / chart_filename
    
    plt.savefig(chart_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    # Veritabanına kaydet
    relative_path = str(chart_path.relative_to(DATA_DIR))
    
    db_chart = Chart(
        dataset_id=dataset_id,
        chart_type=chart_request.chart_type,
        x_column=chart_request.x_column,
        y_column=chart_request.y_column,
        title=chart_request.title,
        image_path=relative_path,
        config_json=chart_request.config_json,
    )
    
    session.add(db_chart)
    session.commit()
    session.refresh(db_chart)
    
    # Audit log
    audit = AuditLog(
        entity="chart",
        entity_id=db_chart.id,
        who=user_id,
        action="create",
    )
    session.add(audit)
    session.commit()
    
    return db_chart


@router.get("/charts/", response_model=List[ChartRead])
async def list_charts(
    dataset_id: Optional[int] = Query(None),
    limit: int = Query(50, le=200),
    session: Session = Depends(get_session),
):
    """Grafikleri listele"""
    statement = select(Chart)
    
    if dataset_id:
        statement = statement.where(Chart.dataset_id == dataset_id)
    
    statement = statement.order_by(Chart.created_at.desc()).limit(limit)
    charts = session.exec(statement).all()
    
    return charts

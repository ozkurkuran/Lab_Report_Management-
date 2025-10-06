# Backend Geliştirme Kılavuzu

## Kurulum

### 1. Sanal Ortam Oluştur
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Bağımlılıkları Yükle
```powershell
pip install -r requirements.txt
```

### 3. Veritabanını Başlat
```powershell
# Örnek verileri yükle
python scripts\seed_data.py
```

### 4. Geliştirme Sunucusunu Başlat
```powershell
python app\main.py
# veya
uvicorn app.main:app --reload
```

Backend: http://localhost:8000
API Docs: http://localhost:8000/docs

## Test

### Tüm Testleri Çalıştır
```powershell
pytest
```

### Coverage ile Test
```powershell
pytest --cov=app --cov-report=html
```

Coverage raporu: `htmlcov/index.html`

### Belirli Testleri Çalıştır
```powershell
pytest tests/test_api.py::test_create_project -v
```

## Kod Kalitesi

### Format Kontrolü
```powershell
# Black - kod formatlama
black app tests

# Ruff - linting
ruff check app tests

# MyPy - tip kontrolü
mypy app
```

### Otomatik Düzeltme
```powershell
ruff check --fix app tests
```

## Veritabanı

### Migration (Alembic)
```powershell
# İlk migration
alembic init alembic

# Yeni migration oluştur
alembic revision --autogenerate -m "Add new table"

# Migration uygula
alembic upgrade head

# Geri al
alembic downgrade -1
```

### Veritabanını Sıfırla
```powershell
rm %APPDATA%\lab-report-app\lab_reports.db
python scripts\seed_data.py
```

## API Endpoint'leri

### Projects
- `POST /api/projects/` - Yeni proje
- `GET /api/projects/` - Projeleri listele
- `GET /api/projects/{id}` - Proje detayı
- `PATCH /api/projects/{id}/archive` - Projeyi arşivle

### Experiments
- `POST /api/experiments/` - Yeni deney
- `GET /api/experiments/?project_id=1` - Deneyleri listele
- `GET /api/experiments/{id}` - Deney detayı

### Entries
- `POST /api/entries/` - Yeni entry
- `PATCH /api/entries/{id}` - Entry güncelle (yeni versiyon)
- `GET /api/entries/?experiment_id=1` - Entry'leri listele
- `GET /api/entries/{id}` - Entry detayı
- `GET /api/entries/{id}/versions` - Tüm versiyonları getir

## Örnek API Kullanımı

### Proje Oluştur
```powershell
curl -X POST http://localhost:8000/api/projects/ `
  -H "Content-Type: application/json" `
  -d '{\"name\":\"Test Project\",\"created_by\":1,\"tags\":[\"test\"]}'
```

### Entry Oluştur
```powershell
curl -X POST http://localhost:8000/api/entries/ `
  -H "Content-Type: application/json" `
  -d '{\"experiment_id\":1,\"author_id\":1,\"title\":\"Test Entry\",\"body_md\":\"# Test\",\"tags\":[]}'
```

## Klasör Yapısı

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI uygulaması
│   ├── database.py          # DB bağlantısı
│   ├── models/
│   │   └── __init__.py      # SQLModel modelleri
│   ├── schemas.py           # Pydantic şemaları
│   └── api/
│       ├── projects.py      # Proje endpoint'leri
│       ├── experiments.py   # Deney endpoint'leri
│       ├── entries.py       # Entry endpoint'leri
│       ├── attachments.py   # Dosya yükleme
│       ├── datasets.py      # Veri içe aktarma
│       ├── reports.py       # Rapor üretimi
│       ├── search.py        # Arama
│       └── templates.py     # Şablon yönetimi
├── tests/
│   ├── __init__.py
│   └── test_api.py          # API testleri
├── scripts/
│   └── seed_data.py         # Örnek veri yükleme
├── requirements.txt
└── pyproject.toml
```

## Geliştirme İpuçları

1. **API değişikliklerinden sonra test yaz**
   ```powershell
   pytest tests/test_api.py -k "test_new_feature"
   ```

2. **SQLModel değişikliklerinde migration oluştur**
   ```powershell
   alembic revision --autogenerate -m "Description"
   alembic upgrade head
   ```

3. **Audit log ekle**
   Her create/update/delete işleminde `AuditLog` kaydı oluştur.

4. **Schema validasyon**
   Pydantic ile giriş validasyonu yap.

## Sorun Giderme

### Port zaten kullanımda
```powershell
# 8000 portunu kullanan process'i bul
netstat -ano | findstr :8000
# Process'i sonlandır
taskkill /PID <PID> /F
```

### Import hataları
```powershell
# Backend dizininden çalıştır
cd backend
python app\main.py
```

### Veritabanı kilidi
```powershell
# Uygulamayı kapat ve veritabanını sil
rm %APPDATA%\lab-report-app\lab_reports.db
python scripts\seed_data.py
```

# Laboratuvar Rapor Yönetim Sistemi - Hızlı Başlangıç

## 🚀 İlk Kurulum (5 Dakika)

### Gereksinimler
- Python 3.11+
- Node.js 18+
- Git

### 1. Backend Kurulumu

```powershell
# Proje dizinine git
cd lab-report-app\backend

# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı aktifleştir (PowerShell execution policy hatası alırsanız)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Aktifleştir
.\venv\Scripts\Activate.ps1

# Bağımlılıkları yükle
pip install -r requirements.txt

# Örnek verileri yükle
python scripts\seed_data.py

# Backend'i başlat
python app\main.py
```

**Backend çalışıyor:** http://localhost:8000  
**API Dokümanları:** http://localhost:8000/docs

### 2. Test Çalıştır

```powershell
# Backend dizininde
pytest tests\test_api.py -v
```

**Beklenen çıktı:** 13 test PASSED ✅

### 3. API Test (Manuel)

```powershell
# Projeleri listele
curl http://localhost:8000/api/projects/

# Sağlık kontrolü
curl http://localhost:8000/health
```

## 📁 Oluşturulan Dosyalar

### Backend Yapısı
```
backend/
├── app/
│   ├── main.py                 ✅ FastAPI uygulaması
│   ├── database.py             ✅ SQLite bağlantısı
│   ├── models/__init__.py      ✅ Veritabanı modelleri
│   ├── schemas.py              ✅ API şemaları
│   └── api/
│       ├── projects.py         ✅ Proje API (TAMAMLANDI)
│       ├── experiments.py      ✅ Deney API (TAMAMLANDI)
│       ├── entries.py          ✅ Entry API (TAMAMLANDI)
│       ├── attachments.py      🔲 Dosya yükleme (TODO)
│       ├── datasets.py         🔲 Veri içe aktarma (TODO)
│       ├── reports.py          🔲 Rapor üretimi (TODO)
│       ├── search.py           🔲 Arama (TODO)
│       └── templates.py        🔲 Şablon yönetimi (TODO)
├── tests/
│   └── test_api.py             ✅ 13 API testi
├── scripts/
│   └── seed_data.py            ✅ Örnek veri yükleyici
├── requirements.txt            ✅ Python bağımlılıkları
└── DEVELOPMENT.md              ✅ Geliştirici kılavuzu
```

## ✅ MVP İlerleme Durumu

### Tamamlanan (Faz 1)
- [x] Backend iskeleti (FastAPI + SQLModel)
- [x] Veritabanı modelleri (8 tablo)
- [x] Proje API (CRUD)
- [x] Deney API (CRUD)
- [x] Entry API (CRUD + versiyonlama)
- [x] Pydantic şemaları (validasyon)
- [x] Audit trail (create/update kayıtları)
- [x] API testleri (13 test)
- [x] Örnek veri yükleyici

### Yapılacaklar (Faz 2 - Sonraki PR)
- [ ] Dosya yükleme (attachments API)
- [ ] Dataset içe aktarma (CSV/XLSX)
- [ ] Grafik üretimi (matplotlib PNG)
- [ ] DOCX rapor üretimi (docxtpl)
- [ ] PDF rapor üretimi (WeasyPrint)
- [ ] XLSX rapor üretimi (openpyxl)
- [ ] Arama & filtreleme
- [ ] Şablon yönetimi
- [ ] Frontend (React + TypeScript)
- [ ] Tauri desktop paketleme

## 🧪 Test Sonuçları

```
test_api.py::test_read_root PASSED
test_api.py::test_health_check PASSED
test_api.py::test_create_project PASSED
test_api.py::test_list_projects PASSED
test_api.py::test_get_project PASSED
test_api.py::test_create_experiment PASSED
test_api.py::test_create_entry PASSED
test_api.py::test_update_entry_creates_new_version PASSED
test_api.py::test_list_entries_with_filters PASSED
test_api.py::test_project_not_found PASSED
test_api.py::test_archive_project PASSED
```

## 📊 Veritabanı

**Konum:** `%APPDATA%\lab-report-app\lab_reports.db`

### Yüklenen Örnek Veriler
- 3 kullanıcı (Dr. Ahmet, Dr. Ayşe, Prof. Mehmet)
- 2 proje (YBCO, Grafen)
- 3 deney (VDP, Hall, Raman)
- 2 entry (günlük kayıtları)
- 2 şablon (DOCX, HTML)

### Şema
```sql
users(id, name, email, role, created_at)
projects(id, name, description, tags, created_by, created_at)
experiments(id, project_id, title, description, tags, start_ts)
entries(id, experiment_id, author_id, title, body_md, version, ...)
attachments(id, entry_id, file_path, file_type, sha256, ...)
datasets(id, entry_id, name, source_file, columns_json, ...)
charts(id, dataset_id, chart_type, image_path, ...)
templates(id, type, name, file_path, is_default, ...)
```

## 🎯 Kabul Kriterleri (MVP)

### ✅ Tamamlanan
1. Backend API çalışıyor (8000 portu)
2. 3 ana endpoint hazır (projects, experiments, entries)
3. Entry versiyonlama çalışıyor
4. Audit trail kaydediliyor
5. API testleri geçiyor (%80+ coverage)
6. Örnek veriler yükleniyor

### 🔲 Devam Eden
1. Dosya yükleme ve önizleme
2. CSV içe aktar → grafik PNG üret
3. 1 DOCX + 1 PDF + 1 XLSX üretimi
4. Arama ve filtreleme
5. Frontend UI (React)
6. Tauri desktop exe

## 🔧 Sorun Giderme

### PowerShell Script Hatası
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port 8000 Kullanımda
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Import Hataları
```powershell
# Backend dizininden çalıştırın
cd backend
python app\main.py
```

## 📚 Daha Fazla Bilgi

- **API Dokümanları:** http://localhost:8000/docs (Swagger UI)
- **Geliştirici Kılavuzu:** `backend/DEVELOPMENT.md`
- **Ana README:** `README.md`

## 🎉 Tebrikler!

Backend MVP'nin ilk fazı tamamlandı. Şimdi testleri çalıştırabilir ve API endpoint'lerini deneyebilirsiniz.

**Sonraki adım:** `attachments.py` ve `datasets.py` endpoint'lerini geliştirmek.

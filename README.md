# 🔬 Laboratuvar Rapor Yönetim Sistemi

> Offline-first, Windows odaklı laboratuvar günlük ve deney raporu uygulaması.

## 🎉 MVP Tamamlandı!

**Faz 1-2-3-3.5 Hazır** ✅
- ✅ **Backend**: 8 modül, 35 endpoint, 13 test (100% geçti)
- ✅ **Frontend**: Vanilla JS ile fonksiyonel UI
- ✅ **Multi-Language**: 🇹🇷 Türkçe + 🇬🇧 İngilizce
- ✅ **Branding**: Mikrofab şirketi logosu
- ✅ **Database**: SQLite + 9 tablo + sample data
- 📋 **Desktop**: Tauri kurulum rehberi hazır (TAURI_SETUP.md)

## 🚀 Hızlı Başlangıç

```powershell
# 1. Backend'i başlat
cd backend
pip install -r requirements.txt
python scripts\seed_data.py
$env:PYTHONPATH="."
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 2. Tarayıcıda aç
# http://127.0.0.1:8000
```

## 🛠️ Teknoloji Yığını

### Backend
- **API Framework**: FastAPI 0.118+
- **ORM**: SQLModel 0.0.25
- **Database**: SQLite (lokal)
- **Validation**: Pydantic v2
- **Data Processing**: Pandas 2.3+, NumPy 2.3+
- **Visualization**: Matplotlib 3.10+
- **Documents**: python-docx 1.2, openpyxl 3.1+
- **Testing**: Pytest 8.4+, httpx

### Frontend
- **Current**: Vanilla HTML/CSS/JavaScript
- **Future**: React + TypeScript + Vite + Tailwind CSS + Radix UI
- **Serving**: FastAPI StaticFiles

### Desktop (Planned)
- **Framework**: Tauri
- **Package**: Windows .exe + MSI installer

## Proje Yapısı

```
lab-report-app/
├── backend/           # FastAPI + Python servisleri
│   ├── app/
│   │   ├── models/    # SQLModel veritabanı modelleri
│   │   ├── api/       # API endpoint'leri
│   │   ├── services/  # İş mantığı (rapor, dataset vb.)
│   │   └── main.py    # FastAPI uygulaması
│   ├── tests/         # Pytest testleri
│   ├── alembic/       # Veritabanı migration'ları
│   └── requirements.txt
├── frontend/          # React + TypeScript UI
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
├── templates/         # DOCX/HTML rapor şablonları
├── storage/           # Yüklenen dosyalar (git'e dahil değil)
└── src-tauri/         # Tauri desktop konfigürasyonu
```

## Geliştirme Ortamı Kurulumu

### Gereksinimler

- Python 3.11+
- Node.js 18+
- Rust (Tauri için)

## 📦 Kurulum

### Gereksinimler
- Python 3.11+
- (Opsiyonel) Node.js 18+ (React versiyonu için)
- (Opsiyonel) Rust (Tauri için)

### Adım 1: Backend + Frontend

```powershell
cd backend

# Virtual environment oluştur (opsiyonel)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Bağımlılıkları yükle
pip install -r requirements.txt

# Sample data yükle
python scripts\seed_data.py

# Sunucuyu başlat
$env:PYTHONPATH="."
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Erişim Adresleri:**
- Frontend: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

### Adım 2: Test Et

```powershell
cd backend
pytest tests\test_api.py -v

# Sonuç: 13 PASSED ✅
```

## Özellikler (MVP)

### ✅ Temel İşlevler (Backend %100 Tamamlandı!)
- [x] Proje/Deney/Entry hiyerarşisi (CRUD)
- [x] Zengin metin (Markdown desteği)
- [x] Dosya yükleme (PNG, JPG, PDF, DOCX, XLSX, CSV) - SHA256 hash
- [x] Dataset içe aktarma (CSV/XLSX + pandas)
- [x] Grafik üretimi (matplotlib - line, scatter, bar, histogram)
- [x] Çoklu kriter arama ve filtreleme
- [x] Entry sürümleme (otomatik versiyon tracking)
- [x] Audit trail (tam değişiklik geçmişi)

### 📄 Rapor Üretimi (Backend Ready!)
- [x] DOCX (python-docx - metadata, resim, grafik)
- [x] XLSX (openpyxl - çoklu sayfa, özet)
- [x] PDF/HTML (basit HTML rendering)
- [x] Toplu dışa aktarma (ZIP - deney + tüm ekler)

### 🔍 Arama & Filtre (Backend + Frontend Ready!)
- [x] Proje, deney, entry arama
- [x] Tam metin arama (başlık + içerik)
- [x] Tag kombinasyonları
- [x] Tarih aralığı ve yazar filtreleme
- [x] Frontend arama sayfası

## API Kullanımı

### Proje Oluşturma
```bash
POST http://localhost:8000/api/projects
Content-Type: application/json

{
  "name": "YBCO Karakterizasyon",
  "description": "Yüksek sıcaklık süperiletken örnekler",
  "tags": ["YBCO", "VDP", "Hall"],
  "created_by": 1
}
```

### Entry Ekleme
```bash
POST http://localhost:8000/api/entries
Content-Type: application/json

{
  "experiment_id": 1,
  "author_id": 1,
  "title": "Günlük-2025-10-06",
  "body_md": "## Deney Koşulları\n- Sıcaklık: 77K\n- Manyetik alan: 0.5T",
  "tags": ["YBCO", "VDP"]
}
```

### DOCX Rapor Üretme
```bash
POST http://localhost:8000/api/reports/docx
Content-Type: application/json

{
  "entry_id": 1,
  "template_id": 1
}
```

## 🧪 Test

```powershell
# Backend testleri
cd backend
pytest tests\test_api.py -v

# Sonuç
# 13 PASSED in 5.40s
# Coverage: 55% (542/981 lines)
```

## 📚 Proje Yapısı

```
lab-report-app/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app + Frontend serving
│   │   ├── database.py          # SQLite connection
│   │   ├── models/__init__.py   # 9 tablo modeli
│   │   ├── schemas.py           # Pydantic validation
│   │   └── api/                 # 8 API modülü (35 endpoint)
│   │       ├── projects.py      # 4 endpoint
│   │       ├── experiments.py   # 3 endpoint
│   │       ├── entries.py       # 5 endpoint
│   │       ├── attachments.py   # 5 endpoint
│   │       ├── datasets.py      # 6 endpoint
│   │       ├── reports.py       # 4 endpoint
│   │       ├── search.py        # 4 endpoint
│   │       └── templates.py     # 4 endpoint
│   ├── tests/
│   │   └── test_api.py          # 13 tests
│   ├── scripts/
│   │   └── seed_data.py         # Sample data loader
│   ├── requirements.txt
│   └── DEVELOPMENT.md
├── frontend/
│   ├── index.html               # All-in-one SPA (HTML+CSS+JS)
│   └── README.md
├── README.md
├── QUICKSTART.md
├── STATUS.md
└── BACKEND_COMPLETE.md
```

## 🗄️ Veritabanı Yapısı (9 Tablo)

| Tablo | Açıklama | Özellikler |
|-------|----------|------------|
| users | Kullanıcılar | Email (unique), isim |
| projects | Projeler | JSON tags, arşivleme |
| experiments | Deneyler | Proje ilişkisi, JSON tags |
| entries | Kayıtlar | **Versiyonlu**, Markdown, parent_version_id |
| attachments | Dosyalar | **SHA256 hash**, file_path, size, type |
| datasets | Veri setleri | **Pandas JSON**, stats (mean/std/min/max) |
| charts | Grafikler | Matplotlib PNG, dataset ilişkisi |
| audit_logs | Değişiklik geçmişi | Entity tracking, diff JSON |
| templates | Rapor şablonları | DOCX/HTML şablonları |

### Öne Çıkan Özellikler
- ✅ **Entry Versioning**: Her güncelleme yeni versiyon oluşturur (v1→v2→v3)
- ✅ **Audit Trail**: Tüm create/update işlemleri loglanır
- ✅ **SHA256 Hash**: Dosya tekrarı önlenir
- ✅ **JSON Fields**: Esnek veri yapıları (tags, columns, stats, diff)

## 📍 Veritabanı Konumu

```
%APPDATA%\lab-report-app\
├── lab_reports.db          # SQLite database
└── storage/
    ├── attachments/        # Yüklenen dosyalar (yyyy/mm/)
    ├── datasets/           # CSV/XLSX dosyaları
    ├── charts/             # Üretilen grafikler
    └── reports/            # Üretilen raporlar
```

## 🎯 Frontend Özellikleri

### Mevcut (Vanilla JS)
- ✅ Dashboard (istatistikler + son kayıtlar)
- ✅ Proje oluşturma + listeleme
- ✅ Deney oluşturma + listeleme
- ✅ Kayıt oluşturma + listeleme + detay
- ✅ Arama (metin + etiket)
- ✅ API dokümantasyonu linkleri
- ✅ Gerçek zamanlı API durumu
- ✅ Responsive design (mobile-friendly)

### Gelecek (React - Opsiyonel)
- ⏳ Drag-drop dosya yükleme
- ⏳ Dataset önizleme tablosu
- ⏳ Grafik oluşturma UI
- ⏳ Markdown editör (syntax highlighting)
- ⏳ Rapor üretme arayüzü
- ⏳ Versiyon karşılaştırma
- ⏳ Gelişmiş arama filtreleri

## 📦 Desktop Paketleme (Gelecek)

Tauri ile Windows .exe oluşturma:

```powershell
# Node.js kurulduktan sonra
cd frontend
npm create vite@latest frontend-react -- --template react-ts
cd frontend-react
npm install
npm install -D @tauri-apps/cli
npm run tauri build
```

Çıktı:
- `lab-report-app.exe` (portable)
- `lab-report-app_x.x.x_x64.msi` (installer)

## 🔒 Güvenlik Notları

- **Lokal Kullanım**: İnternet bağlantısı gerektirmez
- **CORS**: Sadece localhost originlerine izin verilir
- **Offline-First**: Tüm veri lokal SQLite'da saklanır
- Tüm veriler `%APPDATA%/lab-report-app/` altında saklanır
- CORS sadece localhost:5173'e açıktır

## Katkıda Bulunma

1. Backend değişiklikleri için testler ekleyin
2. Code style: `black`, `ruff`, `mypy` (Python), `eslint`, `prettier` (TypeScript)
3. Commit mesajları: `feat:`, `fix:`, `docs:`, `test:` ön ekleri kullanın

## Lisans

MIT

## İletişim

Sorunlar için GitHub Issues kullanın.

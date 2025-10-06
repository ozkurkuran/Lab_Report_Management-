# Laboratuvar Rapor Yönetim Sistemi

Offline-first, Windows odaklı laboratuvar günlük ve deney raporu uygulaması.

## Teknoloji Yığını

- **Frontend**: React + TypeScript + Tailwind CSS + Radix UI
- **Backend**: Python FastAPI + SQLModel + SQLAlchemy
- **Database**: SQLite
- **Desktop**: Tauri
- **Raporlama**: python-docx-template, pandas, openpyxl, WeasyPrint

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

### 1. Backend Kurulumu

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Veritabanını başlat
alembic upgrade head

# Örnek verileri yükle
python scripts/seed_data.py

# Geliştirme sunucusunu başlat
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend: http://localhost:8000
API Docs: http://localhost:8000/docs

### 2. Frontend Kurulumu

```powershell
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

### 3. Tauri Development

```powershell
# Tauri CLI kurulumu (bir kez)
npm install -g @tauri-apps/cli

# Desktop uygulamayı geliştirme modunda çalıştır
npm run tauri dev
```

## Özellikler (MVP)

### ✅ Temel İşlevler
- [x] Proje/Deney/Entry hiyerarşisi
- [x] Zengin metin editörü (Markdown)
- [x] Dosya yükleme (resim, PDF, DOCX, XLSX, CSV)
- [x] Dataset içe aktarma ve grafik üretimi
- [x] Arama ve filtreleme
- [x] Entry sürümleme
- [x] Audit trail

### 📄 Rapor Üretimi
- [x] DOCX (şablon bazlı)
- [x] XLSX (ham veri + özet)
- [x] PDF (HTML → PDF)
- [x] Toplu dışa aktarma (ZIP)

### 🔍 Arama & Filtre
- Proje, deney, tarih aralığı
- Etiket bazlı filtreleme
- Yazar filtreleme
- Tam metin arama

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

## Paketleme (Production Build)

### Windows Executable Üretimi

```powershell
# Frontend build
cd frontend
npm run build

# Tauri build (exe + installer)
npm run tauri build
```

Çıktı: `src-tauri/target/release/bundle/`
- `lab-report-app.exe` (portable)
- `lab-report-app_x.x.x_x64_en-US.msi` (installer)

## Test

```powershell
# Backend testleri
cd backend
pytest tests/ -v --cov=app

# Frontend testleri
cd frontend
npm test
```

## Veritabanı Yapısı

- **users**: Kullanıcılar
- **projects**: Projeler
- **experiments**: Deneyler
- **entries**: Günlük kayıtları (versiyonlu)
- **attachments**: Dosya ekleri
- **datasets**: İçe aktarılan veri setleri
- **audit_logs**: Değişiklik geçmişi
- **templates**: Rapor şablonları

## Güvenlik Notları (MVP)

- Lokal kullanım için tasarlanmıştır
- Ağ erişimi gerektirmez
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

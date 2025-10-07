# Frontend - Laboratuvar Rapor Yönetim Sistemi

## 📋 Genel Bakış

Vanilla HTML/JS/CSS ile oluşturulmuş, hafif ve hızlı bir frontend arayüzü. Node.js gerektirmez, doğrudan FastAPI tarafından sunulur.

## ✨ Özellikler

### 1. Dashboard
- **İstatistikler**: Proje, deney, kayıt ve dosya sayıları
- **Son Kayıtlar**: En son eklenen 5 kayıt
- **Gerçek Zamanlı API Durumu**: Sol altta yeşil/kırmızı gösterge

### 2. Projeler
- Yeni proje oluşturma formu
- Mevcut projeleri listeleme
- Etiket sistemi
- Proje açıklamaları

### 3. Deneyler
- Proje seçimi ile yeni deney ekleme
- Deney listesi görüntüleme
- Etiket bazlı organizasyon

### 4. Kayıtlar (Entries)
- Deney seçimi ile yeni kayıt oluşturma
- Markdown desteği (body_md alanı)
- Versiyon bilgisi görüntüleme
- Detaylı içerik görüntüleme (Details/Summary)
- Etiket filtreleme

### 5. Arama
- Metin bazlı arama (başlık ve içerik)
- Etiket kombinasyonları
- Anlık sonuç gösterimi

### 6. API Dokümantasyonu
- Swagger UI linki
- Hızlı başlangıç komutları
- Endpoint listesi

## 🎨 Tasarım

### Renkler
- **Ana Renk**: Mor-mavi gradient (#667eea → #764ba2)
- **Arka Plan**: Beyaz kartlar (#ffffff)
- **İkincil**: Açık gri (#f8f9fa)
- **Metin**: Koyu gri (#495057)

### Layout
- **Responsive**: Tüm ekran boyutlarına uyumlu
- **Grid System**: CSS Grid ile otomatik sütunlar
- **Card-based**: Her öğe kart tasarımında
- **Smooth Animations**: Fade-in ve hover efektleri

### Bileşenler
- **Nav Tabs**: Üstte sekme navigasyonu
- **Stat Cards**: Renkli istatistik kartları
- **List Items**: Hover ile kaydırma efektli liste öğeleri
- **Forms**: Modern, gradient butonlu formlar
- **Tags**: Renkli, yuvarlak etiketler
- **API Status Badge**: Sağ altta sabit gösterge

## 🚀 Kullanım

### Backend ile Birlikte Çalıştırma

```powershell
# Backend dizinine git
cd backend

# Sunucuyu başlat
$env:PYTHONPATH="."
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Tarayıcıda Açma

Frontend otomatik olarak http://127.0.0.1:8000 adresinde sunulur.

```
http://127.0.0.1:8000           → Frontend
http://127.0.0.1:8000/docs      → Swagger UI
http://127.0.0.1:8000/health    → Health Check
```

## 🔧 Teknik Detaylar

### API İletişimi

```javascript
const API_URL = 'http://localhost:8000';

// Örnek GET request
const projects = await fetch(`${API_URL}/api/projects/`).then(r => r.json());

// Örnek POST request
const response = await fetch(`${API_URL}/api/projects/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});
```

### API Status Kontrolü

Her 10 saniyede bir `/health` endpoint'i kontrol edilir:

```javascript
setInterval(checkApiStatus, 10000);
```

### Veri Yükleme

Her sekme açıldığında ilgili veri otomatik yüklenir:

```javascript
function showTab(tabName) {
    if (tabName === 'dashboard') loadDashboard();
    if (tabName === 'projects') loadProjects();
    if (tabName === 'experiments') loadExperiments();
    if (tabName === 'entries') loadEntries();
}
```

## 📦 Dosya Yapısı

```
frontend/
├── index.html          # Ana sayfa (tüm kod burada)
└── README.md          # Bu dosya
```

### Tek Dosya Yaklaşımı

Tüm HTML, CSS ve JavaScript tek dosyada (`index.html`) bulunur:

- **HTML**: Semantic markup ile sayfa yapısı
- **CSS**: `<style>` tagı içinde tüm stiller
- **JavaScript**: `<script>` tagı içinde tüm logic

**Neden?**
- ✅ Node.js gerektirmez
- ✅ Build tool'suz çalışır
- ✅ Hızlı geliştirme
- ✅ Kolay deploy
- ✅ Minimal bağımlılık

## 🔮 Gelecek Geliştirmeler (Opsiyonel)

### Faz 3b: React + TypeScript (Gelişmiş UI)

Node.js kurulduktan sonra:

```powershell
# Node.js indir: https://nodejs.org/

# Vite + React + TypeScript projesi oluştur
npm create vite@latest frontend-react -- --template react-ts
cd frontend-react
npm install

# Bağımlılıklar
npm install @radix-ui/react-dropdown-menu
npm install @radix-ui/react-dialog
npm install @radix-ui/react-tabs
npm install tailwindcss postcss autoprefixer
npm install react-markdown
npm install axios

# Development server
npm run dev  # http://localhost:5173
```

### Eklenmesi Planlanan Özellikler

1. **Dosya Yükleme UI**: Drag & drop file upload
2. **Dataset Görüntüleme**: Pandas veri tabloları
3. **Chart Oluşturma**: Görsel grafik oluşturma arayüzü
4. **Rapor Üretme**: DOCX/PDF/XLSX export UI
5. **Markdown Editör**: Syntax highlighting
6. **Gelişmiş Arama**: Filtreler ve tarihe göre sıralama
7. **Versiyon Geçmişi**: Entry versiyonlarını karşılaştırma
8. **Template Yönetimi**: Rapor şablonu yükleme/düzenleme

## 📚 API Endpoint'leri

### Projects
- `GET /api/projects/` - Liste
- `POST /api/projects/` - Oluştur
- `GET /api/projects/{id}` - Detay
- `PATCH /api/projects/{id}/archive` - Arşivle

### Experiments
- `GET /api/experiments/` - Liste
- `POST /api/experiments/` - Oluştur
- `GET /api/experiments/{id}` - Detay

### Entries
- `GET /api/entries/` - Liste
- `POST /api/entries/` - Oluştur
- `GET /api/entries/{id}` - Detay
- `PATCH /api/entries/{id}` - Güncelle (yeni versiyon)
- `GET /api/entries/{id}/versions` - Versiyon geçmişi

### Attachments
- `POST /api/attachments/` - Yükle
- `GET /api/attachments/` - Liste
- `GET /api/attachments/{id}` - Detay
- `GET /api/attachments/{id}/download` - İndir
- `DELETE /api/attachments/{id}` - Sil

### Datasets
- `POST /api/datasets/import` - CSV/XLSX içe aktar
- `GET /api/datasets/` - Liste
- `GET /api/datasets/{id}` - Detay
- `GET /api/datasets/{id}/preview` - Önizleme
- `POST /api/datasets/{id}/chart` - Grafik oluştur

### Reports
- `POST /api/reports/docx` - DOCX rapor
- `POST /api/reports/xlsx` - XLSX rapor
- `POST /api/reports/pdf` - PDF/HTML rapor
- `GET /api/reports/experiments/{id}/export` - ZIP export

### Search
- `GET /api/search/entries` - Kayıt ara
- `GET /api/search/all` - Tümünde ara

### Templates
- `GET /api/templates/` - Liste
- `POST /api/templates/` - Yükle
- `DELETE /api/templates/{id}` - Sil

## 🎯 Test Verileri

Backend'de sample data var (seed_data.py):

- **3 Kullanıcı**: Dr. Ahmet, Dr. Ayşe, Prof. Mehmet
- **2 Proje**: YBCO İnce Film, Grafen Nanoşeritler
- **3 Deney**: VDP Ölçümleri, Hall Etkisi, Raman Spektroskopi
- **2 Kayıt**: VDP günlük, Hall günlük

Test verisini yüklemek için:

```powershell
cd backend
python scripts\seed_data.py
```

## 🐛 Troubleshooting

### API Bağlantı Hatası
- Backend çalışıyor mu kontrol et: http://127.0.0.1:8000/health
- CORS ayarları doğru mu?
- Console'da hata var mı? (F12)

### Veri Görünmüyor
- Seed data yüklendi mi?
- Network sekmesinde API çağrıları başarılı mı?
- Console'da JavaScript hatası var mı?

### Stil Bozuk
- Tarayıcı cache'ini temizle (Ctrl+Shift+R)
- CSS yüklenmiş mi kontrol et

### Form Gönderilemedi
- Input alanları boş mu?
- Required alanlar dolu mu?
- Console'da detaylı hata mesajı var

## 🛠️ Geliştirme İpuçları

### Local Development

1. İki terminal aç:
   - Terminal 1: `python -m uvicorn app.main:app --reload` (Backend)
   - Terminal 2: Kod düzenleyici

2. Her kayıtta FastAPI otomatik reload yapar

3. Frontend değişiklikleri için tarayıcıyı yenile (F5)

### Debug

Chrome DevTools kullan (F12):
- **Console**: JavaScript hataları
- **Network**: API çağrıları
- **Elements**: HTML/CSS inceleme
- **Sources**: JavaScript debug

### Performance

Mevcut frontend çok hızlı (vanilla JS):
- No bundling
- No virtual DOM
- Direct DOM manipulation
- Minimal JavaScript (< 10KB)

## 📄 Lisans

MIT License - Mikrofab Lab

---

**Not**: Bu frontend Node.js/npm olmadan çalışacak şekilde tasarlanmıştır. React versiyonu için Node.js kurulumu gereklidir.

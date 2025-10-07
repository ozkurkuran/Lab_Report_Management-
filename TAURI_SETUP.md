# 🖥️ Faz 4: Tauri Desktop Uygulaması Kurulum Rehberi

**Hedef**: Windows .exe uygulaması oluşturma  
**Teknoloji**: Tauri v2 + Rust + WebView2

---

## 📋 Ön Gereksinimler

### 1. Node.js Kurulumu ✅ GEREKLİ

```powershell
# Node.js indirin (LTS versiyonu önerilir)
# https://nodejs.org/en/download/

# Kurulum sonrası kontrol
node --version   # v20.x.x veya üzeri
npm --version    # v10.x.x veya üzeri
```

### 2. Rust Kurulumu ✅ GEREKLİ

```powershell
# Rust installer indirin
# https://www.rust-lang.org/tools/install

# rustup-init.exe çalıştırın ve varsayılan ayarlarla kurun
# Kurulum sonrası terminal'i yeniden başlatın

# Kontrol
rustc --version   # rustc 1.75.0 veya üzeri
cargo --version   # cargo 1.75.0 veya üzeri
```

### 3. Visual Studio C++ Build Tools ✅ GEREKLİ

Tauri, Windows'ta C++ derleyici gerektirir:

```powershell
# Visual Studio Build Tools indirin
# https://visualstudio.microsoft.com/downloads/
# "Build Tools for Visual Studio 2022" seçeneğini indirin

# Kurulumda şunları seçin:
# - Desktop development with C++
# - MSVC v143 - VS 2022 C++ x64/x86 build tools
# - Windows 10/11 SDK
```

**VEYA**

Full Visual Studio 2022 Community Edition kurabilirsiniz (ücretsiz).

### 4. WebView2 Runtime ✅ Windows 11'de Varsayılan

```powershell
# Windows 11'de zaten kurulu
# Windows 10'da yoksa:
# https://developer.microsoft.com/en-us/microsoft-edge/webview2/

# Kontrol (PowerShell)
Get-AppxPackage -Name "Microsoft.WebView2Runtime"
```

---

## 🚀 Adım 1: Frontend Projesini Oluştur

### Vite + React + TypeScript

```powershell
# Proje ana dizininde
cd "c:\Users\ozkur\OneDrive\Mikrofab\Sistemler\Raporlama Yazilimi\lab-report-app"

# React frontend oluştur
npm create vite@latest frontend-react -- --template react-ts

cd frontend-react
npm install
```

### Gerekli Bağımlılıklar

```powershell
# UI kütüphaneleri
npm install @radix-ui/react-dropdown-menu
npm install @radix-ui/react-dialog
npm install @radix-ui/react-tabs
npm install @radix-ui/react-select

# Styling
npm install tailwindcss postcss autoprefixer
npx tailwindcss init -p

# API iletişimi
npm install axios
npm install @tanstack/react-query

# Markdown
npm install react-markdown
npm install remark-gfm

# Icons
npm install lucide-react
```

---

## 🦀 Adım 2: Tauri Ekle

### Tauri CLI Kurulumu

```powershell
cd frontend-react

# Tauri CLI'yi dev dependency olarak ekle
npm install -D @tauri-apps/cli

# Tauri'yi başlat
npm run tauri init
```

### Tauri Init Soruları

```
✔ What is your app name? · Lab Report Management
✔ What should the window title be? · Lab Report Management System
✔ Where are your web assets (HTML/CSS/JS) located? · ../dist
✔ What is the URL of your dev server? · http://localhost:5173
✔ What is your frontend dev command? · npm run dev
✔ What is your frontend build command? · npm run build
```

### package.json'a Script Ekle

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "tauri": "tauri",
    "tauri:dev": "tauri dev",
    "tauri:build": "tauri build"
  }
}
```

---

## 🔧 Adım 3: Tauri Konfigürasyonu

### src-tauri/tauri.conf.json

```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devPath": "http://localhost:5173",
    "distDir": "../dist"
  },
  "package": {
    "productName": "Lab Report Management",
    "version": "1.0.0"
  },
  "tauri": {
    "allowlist": {
      "all": false,
      "shell": {
        "all": false,
        "open": true
      },
      "fs": {
        "all": false,
        "readFile": true,
        "writeFile": true,
        "readDir": true,
        "createDir": true,
        "removeFile": true,
        "exists": true,
        "scope": ["$APPDATA/lab-report-app/*"]
      },
      "dialog": {
        "all": false,
        "open": true,
        "save": true
      },
      "path": {
        "all": true
      }
    },
    "bundle": {
      "active": true,
      "targets": ["msi", "nsis"],
      "identifier": "com.mikrofab.labreport",
      "icon": [
        "icons/32x32.png",
        "icons/128x128.png",
        "icons/128x128@2x.png",
        "icons/icon.icns",
        "icons/icon.ico"
      ],
      "windows": {
        "certificateThumbprint": null,
        "digestAlgorithm": "sha256",
        "timestampUrl": ""
      }
    },
    "security": {
      "csp": null
    },
    "windows": [
      {
        "fullscreen": false,
        "resizable": true,
        "title": "Lab Report Management System - Mikrofab",
        "width": 1400,
        "height": 900,
        "minWidth": 1024,
        "minHeight": 768,
        "center": true
      }
    ]
  }
}
```

---

## 🎨 Adım 4: Icon Oluştur

### Icon Gereksinimleri

Tauri için farklı boyutlarda icon gerekir:

```
src-tauri/icons/
├── 32x32.png
├── 128x128.png
├── 128x128@2x.png
├── icon.icns (macOS)
├── icon.ico (Windows)
└── icon.png (1024x1024)
```

### Icon Oluşturma

```powershell
# Online tool kullanın:
# https://www.npmjs.com/package/@tauri-apps/cli

# VEYA manuel:
# 1. 1024x1024 PNG logo oluşturun (laboratuvar teması)
# 2. https://icon.kitchen/ ile dönüştürün
# 3. src-tauri/icons/ klasörüne kopyalayın
```

**Öneri**: Mikrofab logosunu kullanabilirsiniz veya:
- Mikroskop ikonu
- Deney tüpü ikonu
- Lab notebook ikonu

---

## 🔌 Adım 5: Backend Entegrasyonu

### Backend'i Tauri ile Başlat

Tauri uygulaması açılırken Python backend'ini otomatik başlatmak için:

#### src-tauri/src/main.rs

```rust
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Command, Child};
use tauri::{Manager, Window};

// Backend process tutucusu
struct BackendProcess(Option<Child>);

fn start_backend() -> Result<Child, std::io::Error> {
    #[cfg(target_os = "windows")]
    {
        // Python backend'i başlat
        Command::new("python")
            .args(&[
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000"
            ])
            .current_dir("../backend")
            .spawn()
    }
    
    #[cfg(not(target_os = "windows"))]
    {
        Command::new("python3")
            .args(&[
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000"
            ])
            .current_dir("../backend")
            .spawn()
    }
}

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            // Backend'i başlat
            let backend = start_backend().expect("Failed to start backend");
            app.manage(BackendProcess(Some(backend)));
            
            // Splash screen 2 saniye göster
            std::thread::sleep(std::time::Duration::from_secs(2));
            
            Ok(())
        })
        .on_window_event(|event| match event.event() {
            tauri::WindowEvent::CloseRequested { .. } => {
                // Backend'i kapat
                if let Some(backend_state) = event.window().state::<BackendProcess>().0 {
                    let _ = backend_state.kill();
                }
            }
            _ => {}
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

#### src-tauri/Cargo.toml

```toml
[package]
name = "lab-report-app"
version = "1.0.0"
description = "Lab Report Management System - Mikrofab"
authors = ["Mikrofab"]
license = "MIT"
repository = ""
edition = "2021"

[build-dependencies]
tauri-build = { version = "2.0.0-rc", features = [] }

[dependencies]
tauri = { version = "2.0.0-rc", features = ["shell-open"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

[features]
default = ["custom-protocol"]
custom-protocol = ["tauri/custom-protocol"]
```

---

## 🏗️ Adım 6: Development Build

### Geliştirme Modunda Çalıştır

```powershell
cd frontend-react

# Tauri dev mode
npm run tauri:dev

# Bu şunları yapar:
# 1. Vite dev server başlatır (React hot reload)
# 2. Python backend başlatır
# 3. Tauri window açar
```

**İlk Build Uzun Sürer** (~5-10 dakika):
- Rust bağımlılıkları derlenir
- WebView2 entegrasyonu yapılır

---

## 📦 Adım 7: Production Build

### Release Build Oluştur

```powershell
cd frontend-react

# Production build
npm run tauri:build

# Build süreci:
# 1. Vite production build (React → static files)
# 2. Backend Python dosyaları kopyalanır
# 3. Rust release build
# 4. MSI/NSIS installer oluşturulur
```

### Build Çıktıları

```
src-tauri/target/release/
├── lab-report-app.exe              # Portable executable
└── bundle/
    ├── msi/
    │   └── Lab Report Management_1.0.0_x64_en-US.msi
    └── nsis/
        └── Lab Report Management_1.0.0_x64-setup.exe
```

---

## 🎯 Adım 8: Python Backend Paketleme

### PyInstaller ile Python → EXE

Backend'i .exe'ye dönüştürmek için:

```powershell
cd backend

# PyInstaller kur
pip install pyinstaller

# Spec file oluştur
pyi-makespec app/main.py --name lab-backend --onefile

# Düzenle: lab-backend.spec
# datas=[('app', 'app'), ('storage', 'storage')]

# Build
pyinstaller lab-backend.spec --clean

# Çıktı: dist/lab-backend.exe
```

### Tauri ile Entegrasyon

```rust
// main.rs içinde
fn start_backend() -> Result<Child, std::io::Error> {
    let exe_path = if cfg!(debug_assertions) {
        // Development: Python ile
        "python"
    } else {
        // Production: .exe ile
        "./backend/lab-backend.exe"
    };
    
    Command::new(exe_path)
        .args(&["--host", "127.0.0.1", "--port", "8000"])
        .spawn()
}
```

---

## 🚢 Adım 9: Distribution

### MSI Installer Özellikleri

- ✅ Program Files'a kurulum
- ✅ Başlat menüsüne kısayol
- ✅ Desktop kısayol (opsiyonel)
- ✅ Otomatik güncelleme (opsiyonel)
- ✅ Kaldırma seçeneği

### NSIS Installer (Alternatif)

Daha özelleştirilebilir:
- Custom splash screen
- License agreement
- Component selection
- İlerleme çubuğu

---

## 🔐 Adım 10: Code Signing (Opsiyonel)

### Windows Code Signing Certificate

```powershell
# Sertifika alın (ücretli):
# - DigiCert
# - Sectigo
# - GlobalSign

# tauri.conf.json'da:
"windows": {
  "certificateThumbprint": "YOUR_CERT_THUMBPRINT",
  "digestAlgorithm": "sha256",
  "timestampUrl": "http://timestamp.digicert.com"
}
```

**Not**: Code signing olmadan Windows SmartScreen uyarısı gösterir.

---

## 📋 Tauri Özellikleri

### Avantajlar

- ✅ **Küçük boyut**: ~5-10 MB (Electron: ~150 MB)
- ✅ **Hızlı**: Native WebView2 kullanır
- ✅ **Güvenli**: Rust backend, sandboxed frontend
- ✅ **Cross-platform**: Windows, macOS, Linux
- ✅ **Otomatik güncelleme**: Built-in updater
- ✅ **System tray**: Background çalışma

### Dezavantajlar

- ❌ İlk build uzun (Rust derlemesi)
- ❌ Rust bilgisi gerekir (basit değişiklikler için)
- ❌ WebView2 bağımlılığı (Windows 10/11)

---

## 🛠️ Tauri API Kullanımı

### Frontend'den Tauri API'ye Erişim

```typescript
import { invoke } from '@tauri-apps/api/tauri';
import { open } from '@tauri-apps/api/dialog';
import { appDir } from '@tauri-apps/api/path';

// Rust fonksiyonu çağır
const result = await invoke('greet', { name: 'Mikrofab' });

// File dialog aç
const selected = await open({
  multiple: true,
  filters: [{
    name: 'CSV',
    extensions: ['csv', 'xlsx']
  }]
});

// App directory al
const appDirPath = await appDir();
```

### Rust Backend Komutları

```rust
// src-tauri/src/main.rs

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! Welcome to Mikrofab Lab System", name)
}

#[tauri::command]
fn get_db_path() -> String {
    // Return database path
    let app_dir = tauri::api::path::app_data_dir(&config).unwrap();
    app_dir.join("lab_reports.db").to_str().unwrap().to_string()
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, get_db_path])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

---

## 📊 Build Zamanları

| Platform | Debug Build | Release Build | Installer |
|----------|-------------|---------------|-----------|
| Windows 11 | ~2 dk | ~10 dk | ~2 dk |
| Windows 10 | ~3 dk | ~12 dk | ~2 dk |

**Not**: İlk build çok uzun sürer (Rust dependencies). Sonraki build'ler hızlıdır (incremental compilation).

---

## 🎨 UI Recommendations

### Tauri ile Modern UI

```bash
# Shadcn UI (Tauri uyumlu)
npx shadcn-ui@latest init

# Gerekli componentler
npx shadcn-ui@latest add button
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add table
npx shadcn-ui@latest add dropdown-menu
```

### Mikrofab Branding

```typescript
// src/App.tsx
export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-600">
      <header className="bg-white shadow">
        <div className="flex items-center justify-between p-4">
          <h1 className="text-2xl font-bold">
            🔬 Lab Report Management System
          </h1>
          <p className="text-sm text-gray-600">
            Developed for researchers by Mikrofab
          </p>
        </div>
      </header>
      {/* ... */}
    </div>
  );
}
```

---

## 🐛 Troubleshooting

### Build Hataları

#### 1. Rust not found

```powershell
# Rust yükleyin
# https://rustup.rs/

# PATH'e eklendiğini kontrol edin
rustc --version
```

#### 2. MSVC not found

```powershell
# Visual Studio Build Tools kurun
# Desktop development with C++ seçeneğini ekleyin
```

#### 3. WebView2 Runtime not found

```powershell
# Windows 11'de zaten var
# Windows 10 için indirin:
# https://developer.microsoft.com/microsoft-edge/webview2/
```

#### 4. Python backend başlamıyor

```rust
// main.rs içinde debug ekleyin
println!("Starting backend from: {:?}", current_dir);
```

### Performance İyileştirmeleri

```toml
# Cargo.toml - Release optimizasyonları
[profile.release]
panic = "abort"
codegen-units = 1
lto = true
opt-level = "z"  # Size optimization
strip = true     # Symbol stripping
```

---

## 📚 Kaynaklar

- **Tauri Docs**: https://tauri.app/
- **Tauri Discord**: https://discord.com/invite/tauri
- **Rust Book**: https://doc.rust-lang.org/book/
- **Vite Docs**: https://vitejs.dev/
- **React Docs**: https://react.dev/

---

## ✅ Checklist

### Pre-Development
- [ ] Node.js kuruldu
- [ ] Rust kuruldu
- [ ] Visual Studio Build Tools kuruldu
- [ ] WebView2 Runtime kontrol edildi

### Development
- [ ] React frontend oluşturuldu
- [ ] Tauri init yapıldı
- [ ] Icon'lar eklendi
- [ ] Backend entegrasyonu yapıldı
- [ ] Dev mode test edildi

### Production
- [ ] Release build başarılı
- [ ] MSI installer oluşturuldu
- [ ] Python backend .exe'ye dönüştürüldü
- [ ] Installer test edildi
- [ ] (Opsiyonel) Code signing yapıldı

---

## 🎉 Sonraki Adımlar

1. **Şimdi**: Node.js + Rust kurun
2. **Sonra**: React frontend oluşturun
3. **En Son**: Tauri ile paketleyin

**Tahmini Süre**: 2-3 gün (ilk kez Rust kullanıyorsanız)

---

**Not**: Bu rehber Windows odaklıdır. macOS/Linux için benzer adımlar geçerlidir ama bazı tool'lar değişir.

**Mikrofab © 2025** - Developed for researchers

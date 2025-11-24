# ⚡ Quick Start Guide

Panduan cepat untuk mulai menggunakan Video AI Analyzer.

## 🚀 Setup Cepat (5 Menit)

### 1. Install Dependencies Sistem

```bash
# Mac
brew install ffmpeg tesseract tesseract-lang

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg tesseract-ocr tesseract-ocr-ind
```

### 2. Setup Python Environment

```bash
# Aktifkan virtual environment
source venv/bin/activate

# Install dependencies Python
pip install -r requirements.txt
```

**ATAU** gunakan script setup otomatis:

```bash
chmod +x setup.sh
./setup.sh
```

### 3. Setup Groq API Key

1. Daftar di [https://console.groq.com/](https://console.groq.com/)
2. Ambil API key Anda
3. Buat file `.env`:

```bash
cat > .env << EOF
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768
DOWNLOADS_DIR=downloads
OUTPUT_DIR=output
EOF
```

4. Edit file `.env` dan masukkan API key Anda

## 🎬 Cara Pakai

### Basic Usage

```bash
# Pastikan virtual environment aktif
source venv/bin/activate

# Analisis video
python main.py https://www.youtube.com/watch?v=VIDEO_ID
```

### Pilih Format Output

```bash
# PDF saja
python main.py <url> pdf

# JSON saja  
python main.py <url> json

# Semua format (default)
python main.py <url> all
```

## 📊 Hasil

Setelah selesai, cek folder `output/`:

- `report_*.txt` - Laporan teks
- `report_*.pdf` - Laporan PDF
- `report_*.json` - Data lengkap JSON

## ⚠️ Troubleshooting

**Error: ffmpeg tidak ditemukan**
```bash
brew install ffmpeg  # Mac
```

**Error: tesseract tidak ditemukan**
```bash
brew install tesseract  # Mac
```

**Error: GROQ_API_KEY tidak ditemukan**
- Pastikan file `.env` sudah dibuat
- Pastikan API key sudah diisi

**Proses lambat?**
- Gunakan model Whisper lebih kecil (`tiny` atau `base`)
- Kurangi interval OCR (edit di `main.py`)

## 📖 Dokumentasi Lengkap

Lihat [README.md](README.md) untuk dokumentasi lengkap.

---

**Selamat mencoba! 🎉**


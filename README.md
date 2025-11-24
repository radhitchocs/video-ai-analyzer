# 🎬 Video AI Analyzer

Sistem analisis video otomatis menggunakan AI untuk mendeteksi cyberbullying dan konten berbahaya. Menggunakan Groq API untuk generate laporan AI yang cepat dan akurat.

## 🚀 Fitur

- ✅ Download video dari YouTube atau URL lainnya
- ✅ Ekstrak audio dari video
- ✅ Speech-to-text menggunakan Whisper AI
- ✅ OCR dari frame video menggunakan Tesseract
- ✅ Generate laporan lengkap dengan Groq AI
- ✅ Export ke format TXT, PDF, atau JSON

## 📋 Prerequisites

Sebelum mulai, pastikan sudah terinstall:

1. **Python 3.8+**
2. **ffmpeg** (untuk ekstrak audio)
   ```bash
   # Mac
   brew install ffmpeg
   
   # Linux (Ubuntu/Debian)
   sudo apt-get install ffmpeg
   
   # Windows
   # Download dari https://ffmpeg.org/download.html
   ```

3. **Tesseract OCR** (untuk ekstrak teks dari frame)
   ```bash
   # Mac
   brew install tesseract
   brew install tesseract-lang  # Untuk bahasa Indonesia
   
   # Linux (Ubuntu/Debian)
   sudo apt-get install tesseract-ocr
   sudo apt-get install tesseract-ocr-ind  # Bahasa Indonesia
   
   # Windows
   # Download dari https://github.com/UB-Mannheim/tesseract/wiki
   ```

## 🛠️ Setup Pertama Kali

### 1. Clone atau Download Project

```bash
cd video-ai-analyzer
```

### 2. Buat Virtual Environment (Jika belum ada)

```bash
python3 -m venv venv
```

### 3. Aktifkan Virtual Environment

```bash
# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Catatan:** Whisper akan download model saat pertama kali digunakan (sekitar 150MB untuk model 'base').

### 5. Setup Groq API Key

1. Daftar di [Groq Console](https://console.groq.com/)
2. Ambil API key Anda
3. Copy file `.env.example` menjadi `.env`:
   ```bash
   cp .env.example .env
   ```
4. Edit file `.env` dan masukkan API key Anda:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

### 6. Download Whisper Model (Opsional)

Model akan otomatis didownload saat pertama kali digunakan. Tapi jika ingin download manual:

```python
import whisper
whisper.load_model("base")  # atau "small", "medium", "large"
```

## 📖 Cara Penggunaan

### Basic Usage

```bash
python main.py <video_url>
```

**Contoh:**
```bash
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Pilih Format Output

```bash
# Hanya PDF
python main.py <video_url> pdf

# Hanya JSON
python main.py <video_url> json

# Hanya TXT
python main.py <video_url> txt

# Semua format (default)
python main.py <video_url> all
```

### Contoh Lengkap

```bash
# Aktifkan virtual environment
source venv/bin/activate

# Analisis video
python main.py https://www.youtube.com/watch?v=xxx

# Hasil akan tersimpan di folder output/
```

## 📁 Struktur Project

```
video-ai-analyzer/
├── main.py                 # Script utama
├── video_downloader.py     # Download video dengan yt-dlp
├── audio_extractor.py      # Ekstrak audio dengan ffmpeg
├── speech_to_text.py       # Speech-to-text dengan Whisper
├── ocr_extractor.py        # OCR dari frame video
├── report_generator.py      # Generate laporan dengan Groq
├── pdf_generator.py        # Generate PDF
├── requirements.txt        # Dependencies Python
├── .env.example           # Template konfigurasi
├── .env                   # Konfigurasi (buat sendiri)
├── downloads/             # Folder untuk file sementara
└── output/                # Folder untuk hasil laporan
```

## 🔧 Konfigurasi

Edit file `.env` untuk mengubah konfigurasi:

```env
# Groq API Key (WAJIB)
GROQ_API_KEY=your_groq_api_key_here

# Model Groq (opsional, default: mixtral-8x7b-32768)
GROQ_MODEL=mixtral-8x7b-32768

# Direktori (opsional)
DOWNLOADS_DIR=downloads
OUTPUT_DIR=output
```

## 🎯 Cara Kerja

1. **Download Video** → Download video dari URL menggunakan yt-dlp
2. **Ekstrak Audio** → Ekstrak audio menjadi format WAV menggunakan ffmpeg
3. **Speech-to-Text** → Konversi audio menjadi teks dengan timestamp menggunakan Whisper
4. **OCR Frame** → Ekstrak teks dari frame video menggunakan Tesseract
5. **Generate Laporan** → Kirim semua data ke Groq AI untuk dibuatkan laporan lengkap
6. **Export** → Simpan laporan dalam format TXT, PDF, atau JSON

## 📊 Output

Setelah analisis selesai, Anda akan mendapatkan:

- **report_YYYYMMDD_HHMMSS.txt** → Laporan dalam format teks
- **report_YYYYMMDD_HHMMSS.pdf** → Laporan dalam format PDF
- **report_YYYYMMDD_HHMMSS.json** → Data lengkap dalam format JSON

## ⚙️ Advanced Usage

### Menggunakan Model Whisper yang Lebih Besar

Edit `main.py`, ubah baris:
```python
stt = SpeechToText(model_size="base")  # tiny, base, small, medium, large
```

Semakin besar model = semakin akurat, tapi lebih lambat.

### Mengubah Interval OCR

Edit `main.py`, ubah baris:
```python
ocr_data = extract_text_from_frames(video_path, interval=5)  # Detik
```

### Mengubah Model Groq

Edit `.env`:
```env
GROQ_MODEL=llama-3.1-70b-versatile  # atau model lain yang tersedia
```

## 🐛 Troubleshooting

### Error: ffmpeg tidak ditemukan
```bash
# Install ffmpeg
brew install ffmpeg  # Mac
sudo apt-get install ffmpeg  # Linux
```

### Error: Tesseract tidak ditemukan
```bash
# Install tesseract
brew install tesseract  # Mac
sudo apt-get install tesseract-ocr  # Linux
```

### Error: GROQ_API_KEY tidak ditemukan
- Pastikan file `.env` sudah dibuat dari `.env.example`
- Pastikan API key sudah diisi dengan benar

### Error: Whisper model download gagal
- Cek koneksi internet
- Atau download manual model dari [OpenAI Whisper](https://github.com/openai/whisper)

### Video terlalu besar / proses lambat
- Gunakan model Whisper yang lebih kecil (`tiny` atau `base`)
- Kurangi interval OCR (misalnya dari 5 detik jadi 10 detik)

## 📝 Catatan

- **Groq API**: Gratis dengan rate limit. Cek [Groq Pricing](https://console.groq.com/) untuk detail.
- **Whisper**: Model akan di-cache setelah pertama kali download.
- **File Sementara**: File di folder `downloads/` bisa dihapus setelah analisis selesai.

## 🌐 Deployment (Deploy Gratis!)

Aplikasi ini bisa di-deploy secara **GRATIS** ke berbagai platform cloud!

📖 **Lihat panduan lengkap di [DEPLOYMENT.md](DEPLOYMENT.md)**

### Platform yang Didukung:
- ✅ **Streamlit Cloud** (Paling Mudah - Recommended)
- ✅ **Railway.app**
- ✅ **Render.com**
- ✅ **Fly.io**

Semua file konfigurasi sudah disediakan:
- `Dockerfile` - untuk Railway, Render, Fly.io
- `packages.txt` - untuk Streamlit Cloud
- `render.yaml` - untuk Render auto-config
- `.streamlit/config.toml` - konfigurasi Streamlit

**Quick Start:**
1. Push repo ke GitHub
2. Buka [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect repo dan set environment variables
4. Deploy! 🚀

## 🤝 Kontribusi

Silakan buat issue atau pull request jika ada bug atau fitur baru!

## 📄 License

MIT License

## 🙏 Credits

- [Groq](https://groq.com/) - AI API untuk generate laporan
- [OpenAI Whisper](https://github.com/openai/whisper) - Speech-to-text
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Download video
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR engine

---

**Selamat menggunakan! 🎉**


# 🚀 Cara Run Aplikasi

## ⚠️ Penting: Quote URL!

Di zsh (shell Mac), URL dengan karakter khusus seperti `?` dan `&` harus di-quote:

```bash
# ✅ BENAR - Pakai quote
python main.py "https://youtube.com/shorts/7U8zwdfO-c8?si=UWJPuS-L-V4eA3Jo"

# ❌ SALAH - Tanpa quote
python main.py https://youtube.com/shorts/7U8zwdfO-c8?si=UWJPuS-L-V4eA3Jo
```

## 📋 Langkah-langkah Run

### 1. Aktifkan Virtual Environment

```bash
source venv/bin/activate
```

### 2. Jalankan Analisis Video

```bash
# Format dasar
```python main.py "<video_url>"```

# Contoh dengan YouTube Shorts:
python main.py "https://youtube.com/shorts/7U8zwdfO-c8?si=UWJPuS-L-V4eA3Jo"

# Contoh dengan YouTube biasa:
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Contoh dengan youtu.be:
python main.py "https://youtu.be/EeX-87fcXa0?si=-rk5WXWIsc6XD-4a"
```

### 3. Pilih Format Output (Opsional)

```bash
# Hanya PDF
python main.py "<video_url>" pdf

# Hanya JSON
python main.py "<video_url>" json

# Hanya TXT
python main.py "<video_url>" txt

# Semua format (default)
python main.py "<video_url>" all
```

## 🔧 Troubleshooting

### Error: Whisper Model Download Gagal

Jika ada error saat download Whisper model:

**Solusi 1: Download Model Manual**
```bash
python download_whisper_model.py base
```

**Solusi 2: Gunakan Model Lebih Kecil**
Edit `main.py`, ubah baris 62:
```python
stt = SpeechToText(model_size="tiny")  # Lebih kecil, lebih cepat download
```

**Solusi 3: Hapus File Corrupt dan Coba Lagi**
```bash
rm ~/.cache/whisper/base.pt
python main.py "<video_url>"
```

### Error: zsh: no matches found

Pastikan URL di-quote dengan tanda kutip:
```bash
# ✅ BENAR
python main.py "https://youtube.com/shorts/VIDEO_ID?si=PARAM"

# ❌ SALAH  
python main.py https://youtube.com/shorts/VIDEO_ID?si=PARAM
```

### Error: Download Video Timeout

Jika download video timeout atau gagal:

**Solusi 1: Coba Lagi**
```bash
# File .part yang tidak lengkap akan otomatis dihapus
python main.py "<video_url>"
```

**Solusi 2: Download Manual dengan yt-dlp**
```bash
yt-dlp "<video_url>" -o "downloads/%(title)s.%(ext)s"
```

**Solusi 3: Gunakan Format Lebih Kecil**
Edit `video_downloader.py`, ubah format menjadi:
```python
'format': 'best[height<=480]/worst'  # Format lebih kecil
```

### Error: ffmpeg tidak ditemukan

```bash
brew install ffmpeg
```

### Error: tesseract tidak ditemukan

```bash
brew install tesseract
```

## 📊 Hasil Analisis

Setelah selesai, hasil akan tersimpan di folder `output/`:

- `report_YYYYMMDD_HHMMSS.txt` - Laporan teks
- `report_YYYYMMDD_HHMMSS.pdf` - Laporan PDF  
- `report_YYYYMMDD_HHMMSS.json` - Data lengkap JSON

## ⚠️ Update Model Groq (Penting!)

Jika mendapat error `model_decommissioned`, update model Groq:

```bash
# Update ke model terbaru
python update_groq_model.py llama-3.1-70b-versatile

# Atau pilih model interaktif
python update_groq_model.py
```

Model yang tersedia:
- `llama-3.1-70b-versatile` - Recommended (paling powerful)
- `llama-3.1-8b-instant` - Lebih cepat
- `llama-3.3-70b-versatile` - Versi terbaru

## 💡 Tips

1. **Model Whisper**: 
   - `tiny` - Paling cepat, akurasi rendah
   - `base` - Seimbang (default)
   - `small` - Lebih akurat, lebih lambat
   - `medium` - Sangat akurat, lambat
   - `large` - Paling akurat, sangat lambat

2. **Video Pendek**: Untuk YouTube Shorts atau video pendek (< 1 menit), gunakan model `tiny` atau `base`

3. **Koneksi Internet**: Pastikan koneksi stabil untuk download model Whisper pertama kali

4. **Disk Space**: Model Whisper memakan space:
   - tiny: ~75MB
   - base: ~150MB
   - small: ~500MB
   - medium: ~1.5GB
   - large: ~3GB


# 🔧 Troubleshooting Guide

## Masalah Download Video Timeout

### Gejala
```
[download] Got error: HTTPSConnectionPool(...): Read timed out.
```

### Penyebab
- Koneksi internet lambat atau tidak stabil
- Server YouTube sibuk
- Format video terlalu besar

### Solusi

**1. Coba Lagi (Sudah Otomatis)**
Aplikasi sudah memiliki retry mechanism otomatis (3x attempts):
```bash
python main.py "<video_url>"
```

**2. Hapus File .part yang Tidak Lengkap**
```bash
find downloads -name "*.part" -type f -delete
```

**3. Download Manual dengan yt-dlp**
```bash
yt-dlp "<video_url>" -o "downloads/%(title)s.%(ext)s"
```

**4. Gunakan Format Lebih Kecil**
Edit `video_downloader.py`, ubah format di baris 25:
```python
# Format kecil (480p)
'format': 'best[height<=480]/worst'

# Atau format sangat kecil (360p)
'format': 'worst[ext=mp4]/worst'
```

**5. Cek Koneksi Internet**
```bash
# Test koneksi ke YouTube
ping youtube.com

# Test download speed
curl -o /dev/null https://www.youtube.com
```

## Masalah Whisper Model Download

### Gejala
```
ConnectionResetError: [Errno 54] Connection reset by peer
```

### Solusi

**1. Download Model Manual**
```bash
python download_whisper_model.py base
```

**2. Gunakan Model Lebih Kecil**
Edit `main.py` baris 62:
```python
stt = SpeechToText(model_size="tiny")  # Lebih kecil, lebih cepat
```

**3. Hapus File Corrupt dan Coba Lagi**
```bash
rm ~/.cache/whisper/base.pt
python main.py "<video_url>"
```

## Masalah zsh: no matches found

### Gejala
```
zsh: no matches found: https://...
```

### Solusi
**Selalu quote URL:**
```bash
# ✅ BENAR
python main.py "https://youtube.com/shorts/VIDEO_ID?si=PARAM"

# ❌ SALAH
python main.py https://youtube.com/shorts/VIDEO_ID?si=PARAM
```

## Masalah Dependencies Tidak Ditemukan

### ffmpeg tidak ditemukan
```bash
brew install ffmpeg
```

### tesseract tidak ditemukan
```bash
brew install tesseract
brew install tesseract-lang  # Untuk bahasa Indonesia
```

### Python packages tidak ditemukan
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Masalah Groq API

### Error: GROQ_API_KEY tidak ditemukan
1. Pastikan file `.env` ada
2. Pastikan API key sudah diisi (bukan `your_groq_api_key_here`)
3. Dapatkan API key di: https://console.groq.com/

### Error: Rate limit exceeded
- Groq API gratis memiliki rate limit
- Tunggu beberapa saat sebelum mencoba lagi
- Atau upgrade ke plan berbayar

## Tips Umum

1. **Untuk Video Pendek (< 1 menit)**
   - Gunakan model Whisper `tiny` atau `base`
   - Format video kecil (480p atau lebih kecil)

2. **Untuk Video Panjang (> 10 menit)**
   - Gunakan model Whisper `base` atau `small`
   - Pastikan koneksi internet stabil
   - Pertimbangkan untuk split video menjadi bagian-bagian kecil

3. **Jika Proses Lambat**
   - Gunakan model Whisper lebih kecil
   - Kurangi interval OCR (default: 5 detik)
   - Gunakan format video lebih kecil

4. **Jika Error Berulang**
   - Cek log error dengan detail
   - Pastikan semua dependencies terinstall
   - Coba dengan video lain untuk test
   - Restart terminal dan coba lagi

## Masalah Lainnya?

Jika masalah masih terjadi:
1. Cek file log di folder `output/`
2. Pastikan semua dependencies terinstall dengan benar
3. Coba dengan video yang berbeda
4. Cek dokumentasi lengkap di `README.md`


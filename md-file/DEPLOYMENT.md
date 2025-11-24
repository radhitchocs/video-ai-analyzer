# 🚀 Panduan Deployment Gratis

Panduan lengkap untuk deploy aplikasi Video AI Analyzer secara **GRATIS** ke berbagai platform.

## 📋 Prerequisites

Sebelum deploy, pastikan:
- ✅ Repo sudah di-push ke GitHub (public atau private)
- ✅ Groq API Key sudah siap
- ✅ File konfigurasi sudah ada (sudah disediakan)

## 🎯 Platform Deployment Gratis

### 1. Streamlit Cloud (⭐ Paling Mudah - Recommended)

**Keuntungan:**
- ✅ Gratis untuk public repos
- ✅ Setup sangat mudah
- ✅ Auto-deploy dari GitHub
- ✅ Support system dependencies via `packages.txt`

**Cara Deploy:**

1. **Push repo ke GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Buka [Streamlit Cloud](https://streamlit.io/cloud)**
   - Login dengan GitHub account
   - Klik "New app"

3. **Konfigurasi:**
   - **Repository**: Pilih repo Anda
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: (opsional) custom URL

4. **Set Environment Variables:**
   - Klik "Advanced settings"
   - Tambahkan:
     - `GROQ_API_KEY` = (API key Anda)
     - `GROQ_MODEL` = `mixtral-8x7b-32768` (opsional)
     - `DOWNLOADS_DIR` = `downloads` (opsional)
     - `OUTPUT_DIR` = `output` (opsional)

5. **Deploy!**
   - Klik "Deploy"
   - Tunggu build selesai (sekitar 2-5 menit)
   - Aplikasi akan live di `https://your-app-name.streamlit.app`

**File yang digunakan:**
- `packages.txt` - untuk install ffmpeg dan tesseract
- `.streamlit/config.toml` - konfigurasi Streamlit

---

### 2. Railway.app

**Keuntungan:**
- ✅ Gratis $5 credit per bulan
- ✅ Support Docker
- ✅ Auto-deploy dari GitHub
- ✅ Custom domain gratis

**Cara Deploy:**

1. **Push repo ke GitHub**

2. **Buka [Railway](https://railway.app)**
   - Login dengan GitHub
   - Klik "New Project"
   - Pilih "Deploy from GitHub repo"
   - Pilih repo Anda

3. **Railway akan otomatis detect Dockerfile**
   - Jika tidak, pilih "Dockerfile" sebagai build method

4. **Set Environment Variables:**
   - Klik pada service → Variables
   - Tambahkan:
     ```
     GROQ_API_KEY=your_api_key_here
     GROQ_MODEL=mixtral-8x7b-32768
     DOWNLOADS_DIR=downloads
     OUTPUT_DIR=output
     ```

5. **Deploy!**
   - Railway akan otomatis build dan deploy
   - Dapatkan URL dari dashboard

**File yang digunakan:**
- `Dockerfile` - untuk build container
- `railway.json` - konfigurasi Railway

---

### 3. Render.com

**Keuntungan:**
- ✅ Free tier tersedia
- ✅ Auto-deploy dari GitHub
- ✅ Support Docker atau native Python

**Cara Deploy:**

**Opsi A: Menggunakan Dockerfile (Recommended)**

1. **Push repo ke GitHub**

2. **Buka [Render](https://render.com)**
   - Login dengan GitHub
   - Klik "New +" → "Web Service"
   - Connect GitHub repo

3. **Konfigurasi:**
   - **Name**: video-ai-analyzer
   - **Environment**: Docker
   - **Dockerfile Path**: `Dockerfile`
   - **Plan**: Free

4. **Set Environment Variables:**
   ```
   GROQ_API_KEY=your_api_key_here
   GROQ_MODEL=mixtral-8x7b-32768
   DOWNLOADS_DIR=downloads
   OUTPUT_DIR=output
   ```

5. **Deploy!**

**Opsi B: Menggunakan render.yaml (Auto-config)**

1. **Push repo dengan `render.yaml`**

2. **Buka Render Dashboard**
   - Klik "New +" → "Blueprint"
   - Pilih repo Anda
   - Render akan auto-detect `render.yaml`

3. **Set Environment Variables** (sama seperti di atas)

4. **Deploy!**

**File yang digunakan:**
- `Dockerfile` - untuk build container
- `render.yaml` - konfigurasi Render (opsional)

---

### 4. Fly.io

**Keuntungan:**
- ✅ Free tier dengan limits
- ✅ Global edge network
- ✅ Support Docker

**Cara Deploy:**

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Init project:**
   ```bash
   fly launch
   ```
   - Pilih app name
   - Pilih region
   - Pilih "Dockerfile"

4. **Set secrets (environment variables):**
   ```bash
   fly secrets set GROQ_API_KEY=your_api_key_here
   fly secrets set GROQ_MODEL=mixtral-8x7b-32768
   fly secrets set DOWNLOADS_DIR=downloads
   fly secrets set OUTPUT_DIR=output
   ```

5. **Deploy:**
   ```bash
   fly deploy
   ```

**File yang digunakan:**
- `Dockerfile` - untuk build container

---

## 🔧 Environment Variables

Semua platform memerlukan environment variables berikut:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | ✅ Yes | - | API key dari Groq Console |
| `GROQ_MODEL` | ❌ No | `mixtral-8x7b-32768` | Model Groq yang digunakan |
| `DOWNLOADS_DIR` | ❌ No | `downloads` | Folder untuk file sementara |
| `OUTPUT_DIR` | ❌ No | `output` | Folder untuk hasil laporan |

---

## 📝 Catatan Penting

### ⚠️ Limitations Free Tier

1. **Storage:**
   - File di `downloads/` dan `output/` akan hilang setelah restart
   - Gunakan cloud storage (S3, etc) untuk production

2. **Memory:**
   - Whisper model memerlukan RAM cukup
   - Free tier mungkin terbatas
   - Gunakan model kecil (`tiny`, `base`) untuk free tier

3. **Timeout:**
   - Beberapa platform punya timeout (30-60 detik)
   - Video panjang mungkin timeout
   - Pertimbangkan async processing

4. **Rate Limits:**
   - Groq API punya rate limits
   - Monitor usage di Groq Console

### 💡 Tips Optimasi

1. **Gunakan model Whisper kecil:**
   - Edit `main.py` line 63: `models_to_try = ["tiny", "base"]`

2. **Kurangi interval OCR:**
   - Edit `main.py` line 101: `interval=10` (dari 5 ke 10 detik)

3. **Cleanup files:**
   - Hapus file lama dari `downloads/` dan `output/`

4. **Monitor logs:**
   - Cek logs di platform dashboard untuk error

---

## 🐛 Troubleshooting

### Error: ffmpeg/tesseract not found
- **Streamlit Cloud**: Pastikan `packages.txt` ada dan benar
- **Docker**: Pastikan `Dockerfile` install dependencies dengan benar

### Error: Out of memory
- Gunakan model Whisper lebih kecil
- Kurangi ukuran video yang dianalisis

### Error: Timeout
- Video terlalu panjang
- Pertimbangkan split video atau async processing

### Error: API Key not found
- Pastikan environment variable sudah di-set
- Cek nama variable (case-sensitive)

---

## 🔗 Links Berguna

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [Fly.io Docs](https://fly.io/docs)
- [Groq Console](https://console.groq.com/)

---

## ✅ Checklist Deployment

- [ ] Repo sudah di-push ke GitHub
- [ ] Groq API Key sudah siap
- [ ] File konfigurasi sudah ada (Dockerfile, packages.txt, dll)
- [ ] Environment variables sudah di-set
- [ ] Test aplikasi di local dulu
- [ ] Deploy ke platform pilihan
- [ ] Test aplikasi yang sudah di-deploy
- [ ] Monitor logs untuk error

---

**Selamat deploy! 🎉**

Jika ada masalah, cek logs di platform dashboard atau buat issue di repo.


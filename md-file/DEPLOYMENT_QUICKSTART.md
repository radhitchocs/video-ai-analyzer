# ⚡ Quick Start Deployment

Panduan cepat deploy aplikasi Video AI Analyzer.

## 🎯 Pilihan Tercepat: Streamlit Cloud

### Langkah-langkah:

1. **Push ke GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Buka [streamlit.io/cloud](https://streamlit.io/cloud)**
   - Login dengan GitHub
   - Klik "New app"

3. **Isi form:**
   - Repository: pilih repo Anda
   - Branch: `main`
   - Main file: `app.py`

4. **Set Environment Variables:**
   - Klik "Advanced settings"
   - Tambahkan: `GROQ_API_KEY` = (API key Anda)

5. **Deploy!** 🚀

Aplikasi akan live di: `https://your-app-name.streamlit.app`

---

## 📋 Checklist Sebelum Deploy

- [ ] Repo sudah di GitHub (public atau private)
- [ ] Groq API Key sudah siap
- [ ] File `packages.txt` sudah ada (untuk Streamlit Cloud)
- [ ] File `Dockerfile` sudah ada (untuk Railway/Render/Fly.io)
- [ ] Test aplikasi di local dulu: `streamlit run app.py`

---

## 🔑 Environment Variables

Wajib:
- `GROQ_API_KEY` - Dapatkan di [console.groq.com](https://console.groq.com/)

Opsional:
- `GROQ_MODEL` - Default: `mixtral-8x7b-32768`
- `DOWNLOADS_DIR` - Default: `downloads`
- `OUTPUT_DIR` - Default: `output`

---

## 📖 Panduan Lengkap

Lihat [DEPLOYMENT.md](DEPLOYMENT.md) untuk:
- Detail semua platform
- Troubleshooting
- Tips optimasi
- Advanced configuration

---

**Selamat deploy! 🎉**


# 🎨 Panduan UI - Video AI Analyzer

## 🚀 Cara Menjalankan UI

### 1. Install Dependencies

Pastikan semua dependencies sudah terinstall, termasuk Streamlit:

```bash
# Aktifkan virtual environment
source venv/bin/activate  # Mac/Linux
# atau
venv\Scripts\activate  # Windows

# Install dependencies (termasuk streamlit)
pip install -r requirements.txt
```

### 2. Jalankan Streamlit App

```bash
streamlit run app.py
```

Aplikasi akan otomatis terbuka di browser di `http://localhost:8501`

## 📋 Cara Menggunakan UI

1. **Masukkan URL Video**: Ketik URL video YouTube atau platform lainnya di sidebar
2. **Pilih Format Output**: Pilih format yang diinginkan (all, txt, pdf, atau json)
3. **Klik "Mulai Analisis"**: Proses analisis akan dimulai
4. **Tunggu Proses Selesai**: Progress bar akan menampilkan progress analisis
5. **Download Hasil**: Setelah selesai, download file hasil yang diinginkan

## 🎯 Fitur UI

- ✅ **Input URL Video**: Masukkan URL video dengan mudah
- ✅ **Progress Tracking**: Lihat progress analisis secara real-time
- ✅ **Output Log**: Lihat log proses analisis
- ✅ **Preview Hasil**: Preview laporan sebelum download
- ✅ **Download File**: Download hasil dalam format TXT, PDF, atau JSON
- ✅ **Laporan Terbaru**: Lihat dan download laporan terbaru

## ⚙️ Perbedaan CLI vs UI

### CLI (Command Line)
```bash
python main.py "https://youtube.com/watch?v=xxx"
```

### UI (Web Interface)
```bash
streamlit run app.py
```

**Keduanya menggunakan logic yang sama** - fungsi `analyze_video()` dari `main.py` tidak diubah sama sekali!

## 🔧 Troubleshooting

### UI tidak terbuka
- Pastikan Streamlit sudah terinstall: `pip install streamlit`
- Cek apakah port 8501 sudah digunakan
- Coba jalankan dengan port lain: `streamlit run app.py --server.port 8502`

### Error saat analisis
- Pastikan Groq API Key sudah di-set di file `.env`
- Cek koneksi internet
- Pastikan URL video valid

## 📝 Catatan

- UI menggunakan fungsi `analyze_video()` yang sama dengan CLI
- Semua logic tetap sama, hanya interface yang berbeda
- File hasil tetap disimpan di folder `output/`


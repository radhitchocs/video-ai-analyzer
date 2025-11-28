# 📋 Alur Program Video AI Analyzer

Dokumentasi lengkap alur program dari awal hingga akhir untuk memahami bagaimana sistem bekerja.

---

## 🎯 Overview

Program ini menganalisis video untuk mendeteksi cyberbullying dan konten berbahaya dengan langkah-langkah berikut:

1. **Input**: URL Video (YouTube atau platform lain)
2. **Download**: Mengunduh video ke lokal
3. **Ekstrak Audio**: Memisahkan audio dari video
4. **Speech-to-Text**: Mengkonversi audio menjadi teks dengan timestamp
5. **OCR**: Mengekstrak teks dari frame video
6. **Analisis AI**: Generate laporan dengan Groq AI
7. **Output**: Simpan hasil dalam format TXT, PDF, dan JSON

---

## 🔄 Alur Lengkap Step-by-Step

### **STEP 1: Entry Point & Inisialisasi**

**File**: `app.py` (Streamlit UI) atau `main.py` (CLI)

**Proses**:
1. User memasukkan URL video melalui:
   - **Streamlit UI** (`app.py`): Input di sidebar
   - **CLI** (`main.py`): Argument command line
2. Program memvalidasi URL (harus dimulai dengan `http://` atau `https://`)
3. Program memuat environment variables dari `.env`:
   - `GROQ_API_KEY` (wajib)
   - `GROQ_MODEL` (opsional, default: `llama-3.1-8b-instant`)
   - `DOWNLOADS_DIR` (opsional, default: `downloads`)
   - `OUTPUT_DIR` (opsional, default: `output`)
4. Membuat folder `downloads/` dan `output/` jika belum ada
5. Memanggil fungsi `analyze_video(video_url, output_format)`

**Output**: 
- Folder struktur siap
- Environment variables ter-load
- Siap untuk memproses video

---

### **STEP 2: Download Video**

**File**: `video_downloader.py` → `download_video()`

**Proses**:
1. Program menggunakan library `yt-dlp` untuk download video
2. **Retry Mechanism**: Mencoba download dengan beberapa strategi:
   - **Format Priority**: 
     - Coba format kecil dulu (720p max) untuk menghemat bandwidth
     - Jika gagal, coba format terbaik
   - **Client Strategy** (untuk bypass bot detection):
     - Android client (paling stabil)
     - iOS client
     - Web client
     - Kombinasi Android + iOS
3. **Anti-Bot Detection**:
   - Set custom User-Agent
   - Set HTTP headers yang mirip browser
   - Gunakan referer YouTube
4. Jika download berhasil:
   - File video disimpan di `downloads/`
   - Nama file: `{video_title}.{ext}` (biasanya `.mp4`)
5. Jika semua retry gagal:
   - Tampilkan error message
   - Berikan saran troubleshooting

**Output**: 
- File video di `downloads/{video_title}.mp4`
- Path lengkap ke file video

**Error Handling**:
- Timeout → Retry dengan delay
- Bot detection → Coba client strategy lain
- Format tidak tersedia → Coba format lain
- Network error → Retry hingga 3x

---

### **STEP 3: Ekstrak Audio**

**File**: `audio_extractor.py` → `extract_audio()`

**Proses**:
1. Program menggunakan `ffmpeg` untuk ekstrak audio dari video
2. **Parameter FFmpeg**:
   - `-vn`: No video (hanya audio)
   - `-acodec pcm_s16le`: Audio codec untuk WAV
   - `-ar 16000`: Sample rate 16kHz (optimal untuk Whisper)
   - `-ac 1`: Mono channel (1 channel)
   - `-y`: Overwrite jika file sudah ada
3. Audio diekstrak menjadi format WAV
4. File audio disimpan di `downloads/{video_name}_audio.wav`

**Output**: 
- File audio WAV di `downloads/{video_name}_audio.wav`
- Format: 16kHz, mono, PCM

**Error Handling**:
- `ffmpeg` tidak ditemukan → Error dengan instruksi install
- File video corrupt → Error dengan pesan jelas

---

### **STEP 4: Speech-to-Text (Whisper)**

**File**: `speech_to_text.py` → `SpeechToText.transcribe()`

**Proses**:
1. **Load Model Whisper**:
   - Program mencoba load model dari yang paling akurat ke yang paling kecil:
     - `medium` → `small` → `base` → `tiny`
   - Model di-download otomatis saat pertama kali digunakan
   - Model di-cache di `~/.cache/whisper/`
   - Jika model corrupt, file dihapus dan di-download ulang
2. **Transcribe Audio**:
   - Parameter transcribe:
     - `language="id"`: Bahasa Indonesia
     - `word_timestamps=True`: Dapatkan timestamp per kata
     - `suppress_tokens=[]`: **TIDAK filter kata vulgar** (penting untuk deteksi)
     - `initial_prompt`: Guide model agar tidak filter kata-kata
   - Whisper memproses audio dan menghasilkan transkrip
3. **Format Hasil**:
   - Setiap segmen memiliki:
     - `text`: Teks yang diucapkan
     - `start`: Waktu mulai (detik)
     - `end`: Waktu akhir (detik)
     - `timestamp`: Format `HH:MM:SS`
4. Hasil dikembalikan sebagai list of dict

**Output**: 
- List transkrip dengan format:
  ```python
  [
      {
          "text": "Halo selamat pagi",
          "start": 0.0,
          "end": 2.5,
          "timestamp": "00:00:00"
      },
      ...
  ]
  ```

**Error Handling**:
- Model tidak tersedia → Coba model lebih kecil
- Out of memory → Coba model lebih kecil
- Audio corrupt → Error dengan pesan jelas
- Semua model gagal → Error dengan instruksi download manual

**Catatan Penting**:
- Model `tiny` dan `base` kurang akurat untuk kata slang/vulgar
- Model `medium` direkomendasikan untuk deteksi kata sensitif
- Model `large` paling akurat tapi lambat

---

### **STEP 5: OCR dari Frame Video**

**File**: `ocr_extractor.py` → `extract_text_from_frames()`

**Proses**:
1. **Buka Video**:
   - Menggunakan `cv2.VideoCapture()` untuk membuka video
   - Mendapatkan informasi:
     - FPS (frame per second)
     - Total frames
     - Duration (detik)
2. **Ambil Frame per Interval**:
   - Default interval: **5 detik**
   - Hitung frame interval: `fps * interval`
   - Loop melalui semua frame
   - Ambil frame setiap N frame (sesuai interval)
3. **OCR Processing**:
   - Untuk setiap frame yang diambil:
     - Konversi ke grayscale (lebih baik untuk OCR)
     - Gunakan `pytesseract` untuk OCR
     - Bahasa: `ind+eng` (Indonesia + English)
     - Jika bahasa Indonesia tidak tersedia, fallback ke English
4. **Bersihkan & Filter**:
   - Hanya simpan frame yang memiliki teks (tidak kosong)
   - Format timestamp menjadi `HH:MM:SS`
5. **Format Hasil**:
   - Setiap hasil OCR memiliki:
     - `text`: Teks yang ditemukan
     - `timestamp`: Format `HH:MM:SS`
     - `frame_number`: Nomor frame
     - `timestamp_seconds`: Waktu dalam detik

**Output**: 
- List OCR hasil dengan format:
  ```python
  [
      {
          "text": "HATE SPEECH",
          "timestamp": "00:00:05",
          "frame_number": 150,
          "timestamp_seconds": 5.0
      },
      ...
  ]
  ```

**Error Handling**:
- Video tidak bisa dibuka → Error dengan pesan jelas
- Tesseract tidak ditemukan → Error dengan instruksi install
- Bahasa Indonesia tidak tersedia → Fallback ke English

**Catatan**:
- Interval bisa diubah di `main.py` (default: 5 detik)
- Semakin kecil interval = lebih banyak frame = lebih lama proses
- OCR hanya menangkap teks yang terlihat jelas di video

---

### **STEP 6: Generate Laporan dengan Groq AI**

**File**: `report_generator.py` → `ReportGenerator.generate_report()`

**Proses**:
1. **Inisialisasi Groq Client**:
   - Load `GROQ_API_KEY` dari environment
   - Set model default: `llama-3.1-8b-instant`
   - Siapkan fallback models jika model utama gagal
2. **Gabungkan Data**:
   - Gabungkan semua teks dari:
     - **Speech data**: Transkrip audio dengan timestamp
     - **OCR data**: Teks dari frame video dengan timestamp
   - Format menjadi list dengan source identifier
3. **Buat Prompt untuk AI**:
   - Prompt berisi:
     - Informasi video (judul, durasi, URL)
     - Semua teks yang ditemukan (dari speech + OCR)
     - Instruksi untuk analisis:
       - Deteksi cyberbullying
       - Deteksi ujaran kebencian
       - Deteksi konten vulgar/seksual
       - Deteksi ancaman
       - **PENTING**: Jangan filter kata vulgar, harus dilaporkan apa adanya
   - Format prompt: Structured dengan section jelas
4. **Kirim ke Groq API**:
   - **Model Fallback**: Jika model utama gagal, coba model lain:
     - `llama-3.1-8b-instant`
     - `llama-3.3-70b-versatile`
     - `llama-3.1-70b-versatile`
     - `llama-3.2-90b-versatile`
     - `llama-3.2-11b-versatile`
   - Parameter API:
     - `temperature=0.5`: Balance antara kreativitas dan konsistensi
     - `max_tokens=3000`: Maksimal token untuk laporan lengkap
   - System message: Instruksi untuk AI sebagai ahli analisis konten
5. **Format Laporan**:
   - AI menghasilkan laporan dalam format:
     - **RINGKASAN EKSEKUTIF**
     - **ANALISIS KONTEN**
     - **TEMUAN DETAIL** (jika ada konten berbahaya)
     - **REKOMENDASI**
     - **KESIMPULAN**
   - Laporan dalam bahasa Indonesia, profesional, dan detail

**Output**: 
- String laporan lengkap dalam format teks

**Error Handling**:
- API key tidak ditemukan → Error dengan instruksi setup
- Model decommissioned → Coba model fallback
- Rate limit → Error dengan pesan jelas
- Semua model gagal → Error dengan instruksi update model

**Catatan Penting**:
- AI **TIDAK** akan filter kata vulgar (penting untuk deteksi)
- AI akan melaporkan semua kata vulgar, seksual, atau kasar yang ditemukan
- Laporan menggunakan kutipan langsung dari transkrip

---

### **STEP 7: Generate PDF (Opsional)**

**File**: `pdf_generator.py` → `create_pdf_report()`

**Proses**:
1. **Inisialisasi PDF Generator**:
   - Menggunakan library `fpdf` atau `fpdf2`
   - Set auto page break
2. **Buat Halaman Cover**:
   - Header: "LAPORAN ANALISIS VIDEO AI"
   - Informasi video (judul, URL)
   - Tanggal dan waktu analisis
3. **Tambahkan Isi Laporan**:
   - Parse teks laporan menjadi paragraf
   - Deteksi heading (baris pendek, huruf besar, atau markdown)
   - Format heading dengan font bold
   - Format paragraf dengan font normal
   - **Sanitize text**: 
     - Hapus karakter Unicode yang tidak didukung
     - Konversi fullwidth characters ke ASCII
     - Normalisasi Unicode
4. **Tambahkan Transkrip Lengkap** (opsional):
   - Halaman baru dengan header "TRANSKRIP LENGKAP"
   - List semua segmen audio dengan timestamp
5. **Tambahkan Data OCR** (opsional):
   - Halaman baru dengan header "TEKS DARI VIDEO (OCR)"
   - List semua frame dengan teks yang ditemukan
6. **Simpan PDF**:
   - Simpan di `output/report_{timestamp}.pdf`

**Output**: 
- File PDF di `output/report_{timestamp}.pdf`

**Error Handling**:
- Font encoding error → Sanitize text lebih agresif
- File tidak bisa dibuat → Error dengan pesan jelas

---

### **STEP 8: Simpan Output**

**File**: `main.py` → `analyze_video()`

**Proses**:
1. **Generate Timestamp**:
   - Format: `YYYYMMDD_HHMMSS`
   - Contoh: `20251124_183656`
2. **Simpan Berdasarkan Format**:
   
   **a. Format TXT** (`output_format` = `"txt"` atau `"all"`):
   - Simpan laporan teks langsung ke file
   - Path: `output/report_{timestamp}.txt`
   - Encoding: UTF-8
   
   **b. Format PDF** (`output_format` = `"pdf"` atau `"all"`):
   - Panggil `create_pdf_report()`
   - Path: `output/report_{timestamp}.pdf`
   
   **c. Format JSON** (`output_format` = `"json"` atau `"all"`):
   - Gabungkan semua data:
     - `video_info`: Informasi video (URL, path, title, analyzed_at)
     - `speech_data`: Semua transkrip audio
     - `ocr_data`: Semua hasil OCR
     - `report`: Teks laporan lengkap
   - Simpan sebagai JSON dengan indent 2
   - Path: `output/report_{timestamp}.json`
   - Encoding: UTF-8, `ensure_ascii=False` (support Unicode)

3. **Tampilkan Summary**:
   - Jumlah segmen audio
   - Jumlah frame dengan teks
   - Lokasi file output
   - Preview laporan (20 baris pertama)

**Output**: 
- File-file di folder `output/`:
  - `report_{timestamp}.txt` (jika format txt/all)
  - `report_{timestamp}.pdf` (jika format pdf/all)
  - `report_{timestamp}.json` (jika format json/all)

---

## 📊 Diagram Alur

```
┌─────────────────────────────────────────────────────────────┐
│                    ENTRY POINT                              │
│  app.py (Streamlit UI) atau main.py (CLI)                   │
│  - Input: URL Video                                         │
│  - Validasi URL                                             │
│  - Load Environment Variables                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: DOWNLOAD VIDEO                                     │
│  video_downloader.py → download_video()                     │
│  - yt-dlp dengan retry mechanism                            │
│  - Anti-bot detection                                        │
│  - Output: video.mp4 di downloads/                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: EKSTRAK AUDIO                                      │
│  audio_extractor.py → extract_audio()                       │
│  - ffmpeg: video → audio WAV                                │
│  - Format: 16kHz, mono, PCM                                │
│  - Output: video_audio.wav di downloads/                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: SPEECH-TO-TEXT                                      │
│  speech_to_text.py → SpeechToText.transcribe()              │
│  - Whisper AI (model: medium/small/base/tiny)               │
│  - Bahasa: Indonesia                                        │
│  - No filter (deteksi kata vulgar)                          │
│  - Output: List transkrip dengan timestamp                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: OCR DARI FRAME                                     │
│  ocr_extractor.py → extract_text_from_frames()              │
│  - OpenCV: Buka video                                       │
│  - Tesseract OCR: Ekstrak teks dari frame                   │
│  - Interval: 5 detik                                        │
│  - Output: List teks dari frame dengan timestamp            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: GENERATE LAPORAN                                    │
│  report_generator.py → ReportGenerator.generate_report()    │
│  - Gabungkan speech + OCR data                              │
│  - Buat prompt untuk Groq AI                                │
│  - Kirim ke Groq API (dengan fallback models)                │
│  - Output: Laporan lengkap dalam format teks                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 6: GENERATE PDF (OPSIONAL)                            │
│  pdf_generator.py → create_pdf_report()                     │
│  - FPDF: Buat PDF dari laporan                              │
│  - Tambahkan transkrip lengkap                              │
│  - Tambahkan data OCR                                       │
│  - Output: report_{timestamp}.pdf                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 7: SIMPAN OUTPUT                                       │
│  main.py → analyze_video()                                   │
│  - Generate timestamp                                        │
│  - Simpan TXT (jika dipilih)                                 │
│  - Simpan PDF (jika dipilih)                                 │
│  - Simpan JSON (jika dipilih)                                │
│  - Output: File-file di output/                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 Poin Penting

### **1. Deteksi Kata Vulgar**
- Whisper: `suppress_tokens=[]` dan `initial_prompt` untuk **TIDAK filter** kata vulgar
- Groq AI: System message instruksi untuk **mendeteksi dan melaporkan** semua kata vulgar
- **Tujuan**: Deteksi konten berbahaya, bukan sensor

### **2. Retry Mechanism**
- **Download Video**: 3 retry dengan berbagai strategi
- **Whisper Model**: Fallback ke model lebih kecil jika gagal
- **Groq API**: Fallback ke model lain jika model utama decommissioned

### **3. Error Handling**
- Setiap step memiliki error handling yang jelas
- Error message disertai instruksi troubleshooting
- Program tidak crash, memberikan feedback yang jelas

### **4. Performance**
- **Whisper Model**: Pilih model sesuai kebutuhan (tiny cepat, medium akurat)
- **OCR Interval**: Default 5 detik (bisa diubah untuk balance speed/accuracy)
- **Groq API**: Model `llama-3.1-8b-instant` cepat dan gratis

### **5. Output Format**
- **TXT**: Laporan teks sederhana, mudah dibaca
- **PDF**: Laporan formal dengan transkrip lengkap
- **JSON**: Data lengkap untuk processing lebih lanjut

---

## 📝 Contoh Output

### **TXT Output** (`report_20251124_183656.txt`)
```
LAPORAN ANALISIS VIDEO AI

RINGKASAN EKSEKUTIF
Video ini membahas topik teknologi dengan durasi 5 menit. 
Ditemukan 2 temuan konten yang perlu diperhatikan...

ANALISIS KONTEN
Video membahas tentang backend engineering dengan tone informal...

TEMUAN DETAIL
1. [00:01:23] (Audio): "kamu bodoh banget"
   - Jenis: Penghinaan verbal
   - Tingkat bahaya: Sedang
   ...
```

### **JSON Output** (`report_20251124_183656.json`)
```json
{
  "video_info": {
    "url": "https://youtube.com/watch?v=xxx",
    "title": "Backend is overengineering.mp4",
    "analyzed_at": "2025-11-24T18:36:56"
  },
  "speech_data": [
    {
      "text": "Halo selamat pagi",
      "start": 0.0,
      "end": 2.5,
      "timestamp": "00:00:00"
    }
  ],
  "ocr_data": [
    {
      "text": "HATE SPEECH",
      "timestamp": "00:00:05",
      "frame_number": 150
    }
  ],
  "report": "LAPORAN ANALISIS VIDEO AI\n\n..."
}
```

---

## 🎯 Kesimpulan

Program ini bekerja dengan **7 langkah utama**:
1. Download video dari URL
2. Ekstrak audio dari video
3. Konversi audio menjadi teks (Whisper)
4. Ekstrak teks dari frame video (OCR)
5. Generate laporan dengan AI (Groq)
6. Generate PDF (opsional)
7. Simpan hasil dalam berbagai format

Setiap langkah memiliki **error handling** dan **retry mechanism** untuk memastikan proses berjalan lancar. Program dirancang untuk **mendeteksi konten berbahaya** tanpa filtering, sehingga semua kata vulgar, seksual, atau kasar akan **dilaporkan apa adanya** untuk tujuan analisis.

---

**Dokumentasi ini dibuat untuk membantu memahami alur program secara lengkap dari awal hingga akhir.** 📚


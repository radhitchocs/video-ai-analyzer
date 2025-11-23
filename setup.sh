#!/bin/bash

echo "🚀 Setup Video AI Analyzer"
echo "=========================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 tidak ditemukan. Silakan install Python 3.8+ terlebih dahulu."
    exit 1
fi

echo "✅ Python ditemukan: $(python3 --version)"

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg tidak ditemukan."
    echo "   Install dengan: brew install ffmpeg (Mac) atau apt-get install ffmpeg (Linux)"
    exit 1
fi

echo "✅ ffmpeg ditemukan: $(ffmpeg -version | head -n 1)"

# Check tesseract
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  tesseract tidak ditemukan."
    echo "   Install dengan: brew install tesseract (Mac) atau apt-get install tesseract-ocr (Linux)"
    exit 1
fi

echo "✅ tesseract ditemukan: $(tesseract --version | head -n 1)"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Membuat virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo ""
echo "🔌 Mengaktifkan virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Install dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Membuat file .env..."
    cat > .env << EOF
# Groq API Key
# Dapatkan di: https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here

# Model Groq yang digunakan (default: mixtral-8x7b-32768)
GROQ_MODEL=mixtral-8x7b-32768

# Path untuk menyimpan file sementara
DOWNLOADS_DIR=downloads
OUTPUT_DIR=output
EOF
    echo "✅ File .env dibuat. Jangan lupa isi GROQ_API_KEY!"
else
    echo "✅ File .env sudah ada"
fi

# Create directories
echo ""
echo "📁 Membuat direktori..."
mkdir -p downloads output

echo ""
echo "✅ Setup selesai!"
echo ""
echo "📋 Langkah selanjutnya:"
echo "   1. Edit file .env dan isi GROQ_API_KEY Anda"
echo "   2. Dapatkan API key di: https://console.groq.com/"
echo "   3. Jalankan: python main.py <video_url>"
echo ""


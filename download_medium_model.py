#!/usr/bin/env python3
"""
Script untuk download Whisper model 'medium' secara manual
Model medium lebih akurat untuk menangkap kata slang dan vulgar
"""
import whisper
import sys

def download_model(model_size="medium"):
    """Download Whisper model"""
    print(f"🤖 Downloading Whisper model: {model_size}")
    print("   Ini akan memakan waktu beberapa menit...")
    print()
    
    try:
        model = whisper.load_model(model_size)
        print(f"\n✅ Model '{model_size}' berhasil didownload!")
        print()
        print("📊 Info Model:")
        print(f"   - Size: ~1.5 GB")
        print(f"   - Akurasi: Tinggi")
        print(f"   - Cocok untuk: Deteksi kata sensitif/vulgar/slang")
        print()
        print("💡 Sekarang jalankan main.py, otomatis akan pakai model ini:")
        print("   python main.py <video_url>")
        
    except Exception as e:
        print(f"\n❌ Error saat download model: {str(e)}")
        print()
        print("💡 Solusi:")
        print("   1. Pastikan koneksi internet stabil")
        print("   2. Cek space disk (model ~1.5GB)")
        print("   3. Coba lagi nanti")
        sys.exit(1)

if __name__ == "__main__":
    model_size = sys.argv[1] if len(sys.argv) > 1 else "medium"
    
    if model_size not in ["tiny", "base", "small", "medium", "large"]:
        print(f"❌ Model size tidak valid: {model_size}")
        print("   Pilihan: tiny, base, small, medium, large")
        sys.exit(1)
    
    download_model(model_size)


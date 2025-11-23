#!/usr/bin/env python3
"""
Script untuk download Whisper model secara manual
Berguna jika ada masalah koneksi saat download otomatis
"""
import whisper
import sys

def download_model(model_size="base"):
    """Download Whisper model dengan retry mechanism"""
    print(f"📥 Downloading Whisper model: {model_size}")
    print("   Ini mungkin memakan waktu beberapa menit...")
    print()
    
    try:
        model = whisper.load_model(model_size)
        print(f"✅ Model {model_size} berhasil didownload!")
        print(f"   Lokasi: ~/.cache/whisper/{model_size}.pt")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Tips:")
        print("   - Pastikan koneksi internet stabil")
        print("   - Coba lagi nanti jika ada masalah koneksi")
        print("   - Atau gunakan model yang lebih kecil (tiny)")
        return False

if __name__ == "__main__":
    model_size = sys.argv[1] if len(sys.argv) > 1 else "base"
    
    if model_size not in ["tiny", "base", "small", "medium", "large"]:
        print(f"❌ Model size tidak valid: {model_size}")
        print("   Pilih: tiny, base, small, medium, atau large")
        sys.exit(1)
    
    success = download_model(model_size)
    sys.exit(0 if success else 1)

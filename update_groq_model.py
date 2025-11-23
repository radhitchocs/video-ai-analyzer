#!/usr/bin/env python3
"""
Script untuk update Groq model di file .env
"""
import os
import re

def update_groq_model(new_model="llama-3.1-70b-versatile"):
    """Update GROQ_MODEL di file .env"""
    env_file = ".env"
    
    if not os.path.exists(env_file):
        print("❌ File .env tidak ditemukan!")
        return False
    
    # Baca file .env
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Update atau tambahkan GROQ_MODEL
    if re.search(r'^GROQ_MODEL=', content, re.MULTILINE):
        # Update existing
        content = re.sub(
            r'^GROQ_MODEL=.*$',
            f'GROQ_MODEL={new_model}',
            content,
            flags=re.MULTILINE
        )
        print(f"✅ Model diupdate menjadi: {new_model}")
    else:
        # Tambahkan baru
        content += f"\nGROQ_MODEL={new_model}\n"
        print(f"✅ Model ditambahkan: {new_model}")
    
    # Tulis kembali
    with open(env_file, 'w') as f:
        f.write(content)
    
    return True

if __name__ == "__main__":
    import sys
    
    # Model yang tersedia dan didukung
    available_models = {
        "1": "llama-3.1-70b-versatile",  # Recommended: paling powerful
        "2": "llama-3.1-8b-instant",     # Lebih cepat
        "3": "llama-3.3-70b-versatile",  # Versi terbaru
        "4": "mixtral-8x7b-32768",       # Deprecated (tidak disarankan)
    }
    
    if len(sys.argv) > 1:
        model = sys.argv[1]
    else:
        print("🤖 Update Groq Model")
        print("=" * 40)
        print("Pilih model:")
        print("  1. llama-3.1-70b-versatile (Recommended - Paling powerful)")
        print("  2. llama-3.1-8b-instant (Lebih cepat)")
        print("  3. llama-3.3-70b-versatile (Versi terbaru)")
        print()
        
        choice = input("Pilih nomor (1-3, default: 1): ").strip() or "1"
        model = available_models.get(choice, available_models["1"])
    
    if update_groq_model(model):
        print(f"\n✅ File .env sudah diupdate!")
        print(f"   Model baru: {model}")
        print("\n🚀 Sekarang bisa jalankan aplikasi lagi:")
        print('   python main.py "<video_url>"')
    else:
        print("\n❌ Gagal update model")
        sys.exit(1)


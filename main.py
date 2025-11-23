"""
Script utama untuk analisis video dengan AI
Menggabungkan semua modul: download, audio extract, speech-to-text, OCR, dan report generation
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Import modul-modul kita
from video_downloader import download_video
from audio_extractor import extract_audio
from speech_to_text import SpeechToText
from ocr_extractor import extract_text_from_frames
from report_generator import ReportGenerator
from pdf_generator import create_pdf_report

# Load environment variables
load_dotenv()


def analyze_video(video_url: str, output_format: str = "all"):
    """
    Analisis video lengkap dari URL hingga menghasilkan laporan
    
    Args:
        video_url: URL video (YouTube, dll)
        output_format: Format output ('txt', 'pdf', 'json', 'all')
    """
    print("="*60)
    print("🎬 VIDEO AI ANALYZER - Sistem Analisis Video dengan AI")
    print("="*60)
    print()
    
    # Setup direktori
    downloads_dir = os.getenv("DOWNLOADS_DIR", "downloads")
    output_dir = os.getenv("OUTPUT_DIR", "output")
    Path(downloads_dir).mkdir(parents=True, exist_ok=True)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    video_info = {
        "url": video_url,
        "analyzed_at": datetime.now().isoformat()
    }
    
    try:
        # Step 1: Download video
        print("\n[1/5] 📥 Download Video...")
        video_path = download_video(video_url, downloads_dir)
        video_info["video_path"] = video_path
        video_info["title"] = os.path.basename(video_path)
        
        # Step 2: Ekstrak audio
        print("\n[2/5] 🎵 Ekstrak Audio...")
        audio_path = extract_audio(video_path, downloads_dir)
        
        # Step 3: Speech-to-text dengan Whisper
        print("\n[3/5] 🎤 Speech-to-Text (Whisper)...")
        try:
            stt = SpeechToText(model_size="base")  # Bisa diganti ke 'small' atau 'medium' untuk akurasi lebih tinggi
            speech_data = stt.transcribe(audio_path, language="id")
        except Exception as e:
            print(f"\n⚠️  Error saat load Whisper model: {str(e)}")
            print("\n💡 Mencoba dengan model 'base' yang lebih kecil...")
            try:
                stt = SpeechToText(model_size="base")
                speech_data = stt.transcribe(audio_path, language="id")
            except Exception as e2:
                print(f"\n❌ Masih error: {str(e2)}")
                print("\n📝 Silakan download model secara manual:")
                print("   python -c \"import whisper; whisper.load_model('base')\"")
                raise
        
        # Step 4: OCR dari frame video
        print("\n[4/5] 📸 OCR dari Frame Video...")
        ocr_data = extract_text_from_frames(video_path, interval=5, output_dir=downloads_dir)
        
        # Step 5: Generate laporan dengan Groq
        print("\n[5/5] 🤖 Generate Laporan dengan Groq AI...")
        report_gen = ReportGenerator()
        report_text = report_gen.generate_report(speech_data, ocr_data, video_info)
        
        # Simpan hasil
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"report_{timestamp}"
        
        # Simpan sebagai teks
        if output_format in ["txt", "all"]:
            txt_path = os.path.join(output_dir, f"{base_name}.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(report_text)
            print(f"✅ Laporan teks disimpan: {txt_path}")
        
        # Simpan sebagai PDF
        if output_format in ["pdf", "all"]:
            pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
            create_pdf_report(report_text, pdf_path, video_info)
        
        # Simpan sebagai JSON
        if output_format in ["json", "all"]:
            json_path = os.path.join(output_dir, f"{base_name}.json")
            json_data = {
                "video_info": video_info,
                "speech_data": speech_data,
                "ocr_data": ocr_data,
                "report": report_text
            }
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Data JSON disimpan: {json_path}")
        
        print("\n" + "="*60)
        print("✅ ANALISIS SELESAI!")
        print("="*60)
        print(f"\n📊 Ringkasan:")
        print(f"   - Segmen audio: {len(speech_data)}")
        print(f"   - Frame dengan teks: {len(ocr_data)}")
        print(f"   - Laporan tersimpan di: {output_dir}/")
        
        # Tampilkan preview laporan
        print("\n📝 Preview Laporan:")
        print("-" * 60)
        preview_lines = report_text.split('\n')[:20]
        for line in preview_lines:
            print(line)
        if len(report_text.split('\n')) > 20:
            print("...")
        print("-" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python main.py <video_url> [output_format]")
        print("\nContoh:")
        print("  python main.py https://www.youtube.com/watch?v=xxx")
        print("  python main.py https://www.youtube.com/watch?v=xxx pdf")
        print("\nOutput format: txt, pdf, json, all (default: all)")
        sys.exit(1)
    
    video_url = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "all"
    
    if output_format not in ["txt", "pdf", "json", "all"]:
        print(f"❌ Format output tidak valid: {output_format}")
        print("   Pilih: txt, pdf, json, atau all")
        sys.exit(1)
    
    analyze_video(video_url, output_format)


if __name__ == "__main__":
    main()


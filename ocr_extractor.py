"""
Modul untuk ekstrak teks dari frame video menggunakan OCR (Tesseract)
"""
import cv2
import pytesseract
from pathlib import Path
import os


def extract_text_from_frames(video_path: str, interval: int = 5, output_dir: str = "downloads") -> list:
    """
    Ekstrak teks dari frame video menggunakan OCR
    
    Args:
        video_path: Path ke file video
        interval: Interval detik untuk mengambil frame (default: 5 detik)
        output_dir: Direktori untuk menyimpan frame sementara
        
    Returns:
        List of dict dengan format:
        [
            {
                "text": "teks yang ditemukan",
                "timestamp": "00:00:05",
                "frame_number": 150
            },
            ...
        ]
    """
    # Buat folder jika belum ada
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        print(f"📸 Mengekstrak teks dari frame video...")
        
        # Buka video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception(f"Tidak bisa membuka video: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        print(f"   Video info: {duration:.2f} detik, {fps:.2f} fps")
        
        ocr_results = []
        frame_interval = int(fps * interval)  # Frame setiap N detik
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Ambil frame setiap interval detik
            if frame_count % frame_interval == 0:
                timestamp_seconds = frame_count / fps if fps > 0 else 0
                timestamp = _format_timestamp(timestamp_seconds)
                
                # Lakukan OCR pada frame
                # Konversi ke grayscale untuk OCR yang lebih baik
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # OCR dengan Tesseract
                # Gunakan bahasa Indonesia jika tersedia
                try:
                    text = pytesseract.image_to_string(
                        gray,
                        lang='ind+eng'  # Indonesia + English
                    )
                except:
                    # Fallback ke English jika bahasa Indonesia tidak tersedia
                    text = pytesseract.image_to_string(gray, lang='eng')
                
                # Bersihkan teks
                text = text.strip()
                
                # Hanya simpan jika ada teks yang ditemukan
                if text:
                    ocr_results.append({
                        "text": text,
                        "timestamp": timestamp,
                        "frame_number": frame_count,
                        "timestamp_seconds": timestamp_seconds
                    })
                    print(f"   [{timestamp}] Ditemukan teks: {text[:50]}...")
            
            frame_count += 1
        
        cap.release()
        
        print(f"✅ OCR selesai. Ditemukan {len(ocr_results)} frame dengan teks.")
        return ocr_results
        
    except Exception as e:
        print(f"❌ Error saat ekstrak OCR: {str(e)}")
        raise


def _format_timestamp(seconds: float) -> str:
    """Format detik menjadi format HH:MM:SS"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


if __name__ == "__main__":
    # Test
    video_file = input("Masukkan path video: ")
    results = extract_text_from_frames(video_file, interval=5)
    
    print("\n📝 Hasil OCR:")
    for result in results:
        print(f"[{result['timestamp']}] {result['text']}")


"""
Modul untuk download video dari YouTube atau URL lainnya menggunakan yt-dlp
"""
import os
import yt_dlp
from pathlib import Path
import time


def download_video(video_url: str, output_dir: str = "downloads", max_retries: int = 3) -> str:
    """
    Download video dari URL menggunakan yt-dlp dengan retry mechanism
    
    Args:
        video_url: URL video (YouTube, dll)
        output_dir: Direktori untuk menyimpan video
        max_retries: Jumlah maksimal retry jika download gagal
        
    Returns:
        Path ke file video yang didownload
    """
    # Buat folder jika belum ada
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Format prioritas: coba format terbaik dulu, jika gagal coba format lebih kecil
    format_options = [
        'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]/best[height<=720]',  # Format kecil dulu
        'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Format terbaik
    ]
    
    for attempt in range(max_retries):
        for format_choice in format_options:
            # Konfigurasi yt-dlp dengan timeout lebih panjang
            ydl_opts = {
                'format': format_choice,
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'socket_timeout': 60,  # Timeout 60 detik
                'retries': 5,  # Retry 5 kali per format
                'fragment_retries': 5,  # Retry untuk fragment
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web']  # Gunakan client yang lebih stabil
                    }
                },
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    if attempt > 0:
                        print(f"   Retry attempt {attempt + 1}/{max_retries}...")
                    
                    print(f"📥 Downloading video dari: {video_url}")
                    # Download video
                    info = ydl.extract_info(video_url, download=True)
                    video_filename = ydl.prepare_filename(info)
                    
                    # Jika file tidak ada, coba cari dengan ekstensi yang berbeda
                    if not os.path.exists(video_filename):
                        # Cari file dengan nama yang sama tapi ekstensi berbeda
                        base_name = os.path.splitext(video_filename)[0]
                        for ext in ['.mp4', '.webm', '.mkv', '.m4a']:
                            potential_file = base_name + ext
                            if os.path.exists(potential_file):
                                video_filename = potential_file
                                break
                    
                    # Verifikasi file benar-benar ada dan tidak kosong
                    if os.path.exists(video_filename) and os.path.getsize(video_filename) > 0:
                        print(f"✅ Video berhasil didownload: {video_filename}")
                        return video_filename
                    else:
                        raise Exception("File video tidak ditemukan atau kosong")
                        
            except Exception as e:
                error_msg = str(e)
                # Jika bukan error terakhir, coba lagi
                if attempt < max_retries - 1:
                    if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
                        print(f"⚠️  Timeout saat download (attempt {attempt + 1}/{max_retries})")
                        print(f"   Error: {error_msg}")
                        print(f"   Menunggu 10 detik sebelum retry...")
                        time.sleep(10)
                        continue
                    elif "format" in error_msg.lower():
                        # Format tidak tersedia, coba format berikutnya
                        continue
                    else:
                        print(f"⚠️  Error: {error_msg}")
                        print(f"   Retry dalam 5 detik...")
                        time.sleep(5)
                        continue
                else:
                    # Semua retry gagal
                    print(f"❌ Error saat download video setelah {max_retries} attempts: {error_msg}")
                    print("\n💡 Solusi:")
                    print("   1. Cek koneksi internet Anda")
                    print("   2. Coba lagi nanti (mungkin server YouTube sibuk)")
                    print("   3. Coba dengan video lain")
                    print("   4. Atau download manual dengan yt-dlp:")
                    print(f"      yt-dlp '{video_url}' -o 'downloads/%(title)s.%(ext)s'")
                    raise
    
    # Fallback: jika semua gagal
    raise Exception(f"Gagal download video setelah {max_retries} attempts")


if __name__ == "__main__":
    # Test
    test_url = input("Masukkan URL video: ")
    download_video(test_url)


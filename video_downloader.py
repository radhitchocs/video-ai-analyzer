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
    
    # Strategy untuk bypass bot detection: coba dengan client yang berbeda
    client_strategies = [
        ['android'],  # Strategy 1: Android client (paling stabil)
        ['ios'],      # Strategy 2: iOS client
        ['web'],      # Strategy 3: Web client
        ['android', 'ios'],  # Strategy 4: Coba android dulu, lalu ios
    ]
    
    for attempt in range(max_retries):
        for strategy_idx, client_list in enumerate(client_strategies):
            for format_choice in format_options:
                # Konfigurasi yt-dlp dengan timeout lebih panjang dan anti-bot detection
                ydl_opts = {
                    'format': format_choice,
                    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                    'quiet': False,
                    'no_warnings': False,
                    'socket_timeout': 60,  # Timeout 60 detik
                    'retries': 3,  # Retry 3 kali per format
                    'fragment_retries': 3,  # Retry untuk fragment
                    # Anti-bot detection options
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'referer': 'https://www.youtube.com/',
                    'extractor_args': {
                        'youtube': {
                            'player_client': client_list,  # Gunakan client dari strategy
                        }
                    },
                    # Additional options untuk bypass bot detection
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-us,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate',
                        'Connection': 'keep-alive',
                    },
                }
            
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        if attempt > 0 or strategy_idx > 0:
                            print(f"   Retry attempt {attempt + 1}/{max_retries} (strategy {strategy_idx + 1}/{len(client_strategies)})...")
                        
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
                    
                    # Skip jika error format (coba format lain)
                    if "format" in error_msg.lower() or "requested format" in error_msg.lower():
                        continue  # Coba format berikutnya
                    
                    # Skip jika error bot detection tapi masih ada strategy lain
                    if ("bot" in error_msg.lower() or "sign in" in error_msg.lower() or "cookies" in error_msg.lower()):
                        if strategy_idx < len(client_strategies) - 1:
                            print(f"⚠️  Bot detection terdeteksi, coba strategy lain...")
                            time.sleep(3)  # Delay singkat sebelum coba strategy lain
                            continue  # Coba strategy berikutnya
                    
                    # Jika bukan error terakhir, coba lagi
                    if attempt < max_retries - 1:
                        if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
                            print(f"⚠️  Timeout saat download (attempt {attempt + 1}/{max_retries})")
                            print(f"   Error: {error_msg[:200]}...")
                            print(f"   Menunggu 10 detik sebelum retry...")
                            time.sleep(10)
                            break  # Break dari format loop, coba attempt berikutnya
                        else:
                            print(f"⚠️  Error: {error_msg[:200]}...")
                            print(f"   Retry dalam 5 detik...")
                            time.sleep(5)
                            # Jika sudah semua strategy, baru break
                            if strategy_idx >= len(client_strategies) - 1:
                                break
                            continue
                    else:
                        # Semua retry gagal
                        print(f"❌ Error saat download video setelah {max_retries} attempts: {error_msg[:200]}...")
                        print("\n💡 Solusi:")
                        print("   1. Cek koneksi internet Anda")
                        print("   2. Coba lagi nanti (mungkin server YouTube sibuk)")
                        print("   3. Coba dengan video lain")
                        print("   4. Update yt-dlp: pip install --upgrade yt-dlp")
                        print("   5. Atau download manual dengan yt-dlp:")
                        print(f"      yt-dlp '{video_url}' -o 'downloads/%(title)s.%(ext)s'")
                        raise
    
    # Fallback: jika semua gagal
    raise Exception(f"Gagal download video setelah {max_retries} attempts")


if __name__ == "__main__":
    # Test
    test_url = input("Masukkan URL video: ")
    download_video(test_url)


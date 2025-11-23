"""
Modul untuk ekstrak audio dari video menggunakan ffmpeg
"""
import os
import subprocess
from pathlib import Path


def extract_audio(video_path: str, output_dir: str = "downloads") -> str:
    """
    Ekstrak audio dari video menjadi file WAV menggunakan ffmpeg
    
    Args:
        video_path: Path ke file video
        output_dir: Direktori untuk menyimpan audio
        
    Returns:
        Path ke file audio yang diekstrak
    """
    # Buat folder jika belum ada
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate nama file audio
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(output_dir, f"{video_name}_audio.wav")
    
    try:
        print(f"🎵 Mengekstrak audio dari video...")
        
        # Gunakan ffmpeg untuk ekstrak audio
        # Format: ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 output.wav
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # Audio codec
            '-ar', '16000',  # Sample rate 16kHz (optimal untuk Whisper)
            '-ac', '1',  # Mono channel
            '-y',  # Overwrite output file
            audio_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        if os.path.exists(audio_path):
            print(f"✅ Audio berhasil diekstrak: {audio_path}")
            return audio_path
        else:
            raise Exception("File audio tidak berhasil dibuat")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error saat ekstrak audio: {e.stderr}")
        raise
    except FileNotFoundError:
        print("❌ Error: ffmpeg tidak ditemukan. Pastikan ffmpeg sudah terinstall.")
        print("   Install dengan: brew install ffmpeg (Mac) atau apt-get install ffmpeg (Linux)")
        raise
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    # Test
    test_video = input("Masukkan path video: ")
    extract_audio(test_video)


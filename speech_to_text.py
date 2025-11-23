"""
Modul untuk konversi speech-to-text menggunakan Whisper
"""
import whisper
import os
import time


class SpeechToText:
    def __init__(self, model_size: str = "base", max_retries: int = 3):
        """
        Inisialisasi Whisper model
        
        Args:
            model_size: Ukuran model ('tiny', 'base', 'small', 'medium', 'large')
                       Semakin besar, semakin akurat tapi lebih lambat
            max_retries: Jumlah maksimal retry saat download model
        """
        print(f"🤖 Loading Whisper model: {model_size}")
        
        # Hapus file corrupt jika ada
        cache_dir = os.path.expanduser("~/.cache/whisper")
        model_file = os.path.join(cache_dir, f"{model_size}.pt")
        if os.path.exists(model_file):
            try:
                # Cek apakah file corrupt dengan mencoba load
                import torch
                try:
                    torch.load(model_file, map_location="cpu")
                except:
                    print(f"⚠️  File model corrupt terdeteksi, menghapus...")
                    os.remove(model_file)
            except:
                pass
        
        # Retry mechanism untuk download model
        for attempt in range(max_retries):
            try:
                self.model = whisper.load_model(model_size)
                print("✅ Model Whisper siap digunakan")
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    print(f"⚠️  Error saat load model (attempt {attempt + 1}/{max_retries}): {str(e)}")
                    print(f"   Retry dalam {wait_time} detik...")
                    time.sleep(wait_time)
                    
                    # Hapus file yang mungkin corrupt
                    if os.path.exists(model_file):
                        try:
                            os.remove(model_file)
                        except:
                            pass
                else:
                    print(f"❌ Error saat load model setelah {max_retries} attempts: {str(e)}")
                    print("\n💡 Solusi:")
                    print("   1. Cek koneksi internet Anda")
                    print("   2. Coba jalankan lagi nanti")
                    print("   3. Atau download model secara manual:")
                    print(f"      python -c \"import whisper; whisper.load_model('{model_size}')\"")
                    print("   4. Atau gunakan model yang lebih kecil (tiny) untuk test")
                    raise
    
    def transcribe(self, audio_path: str, language: str = "id") -> list:
        """
        Transcribe audio menjadi teks dengan timestamp
        
        Args:
            audio_path: Path ke file audio
            language: Bahasa audio (default: 'id' untuk Indonesia)
            
        Returns:
            List of dict dengan format:
            [
                {
                    "text": "teks yang diucapkan",
                    "start": 0.0,
                    "end": 5.2,
                    "timestamp": "00:00:00"
                },
                ...
            ]
        """
        try:
            print(f"🎤 Transcribing audio: {audio_path}")
            
            # Transcribe dengan Whisper
            result = self.model.transcribe(
                audio_path,
                language=language,
                word_timestamps=True
            )
            
            # Format hasil menjadi list dengan timestamp
            segments = []
            for segment in result["segments"]:
                start_time = segment["start"]
                end_time = segment["end"]
                
                # Format timestamp menjadi HH:MM:SS
                timestamp = self._format_timestamp(start_time)
                
                segments.append({
                    "text": segment["text"].strip(),
                    "start": start_time,
                    "end": end_time,
                    "timestamp": timestamp
                })
            
            print(f"✅ Transkripsi selesai. Ditemukan {len(segments)} segmen.")
            return segments
            
        except Exception as e:
            print(f"❌ Error saat transcribe: {str(e)}")
            raise
    
    def _format_timestamp(self, seconds: float) -> str:
        """Format detik menjadi format HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


if __name__ == "__main__":
    # Test
    stt = SpeechToText(model_size="base")
    audio_file = input("Masukkan path audio: ")
    result = stt.transcribe(audio_file)
    
    print("\n📝 Hasil Transkripsi:")
    for seg in result:
        print(f"[{seg['timestamp']}] {seg['text']}")


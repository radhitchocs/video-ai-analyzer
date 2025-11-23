"""
Modul untuk generate laporan analisis menggunakan Groq API
"""
import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ReportGenerator:
    def __init__(self):
        """Inisialisasi Groq client"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY tidak ditemukan di environment variables!")
        
        self.client = Groq(api_key=api_key)
        # Model default: llama-3.1-8b-instant (masih aktif dan cepat)
        # Alternatif yang mungkin aktif: llama-3.3-70b-versatile, llama-3.1-70b-versatile
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        # List model fallback jika model utama gagal
        self.fallback_models = [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile", 
            "llama-3.1-70b-versatile",
            "llama-3.2-90b-versatile",
            "llama-3.2-11b-versatile",
        ]
        print(f"✅ Groq client initialized dengan model: {self.model}")
    
    def generate_report(self, speech_data: list, ocr_data: list, video_info: dict = None) -> str:
        """
        Generate laporan analisis cyberbullying dari data yang dikumpulkan
        
        Args:
            speech_data: List hasil transkripsi audio
            ocr_data: List hasil OCR dari frame video
            video_info: Informasi video (opsional)
            
        Returns:
            String laporan lengkap dalam format teks
        """
        print("🤖 Generating laporan dengan Groq AI...")
        
        # Gabungkan semua teks untuk analisis
        all_texts = []
        
        # Tambahkan teks dari speech
        for seg in speech_data:
            all_texts.append({
                "source": "speech",
                "text": seg["text"],
                "timestamp": seg["timestamp"]
            })
        
        # Tambahkan teks dari OCR
        for ocr in ocr_data:
            all_texts.append({
                "source": "ocr",
                "text": ocr["text"],
                "timestamp": ocr["timestamp"]
            })
        
        # Buat prompt untuk Groq
        prompt = self._create_prompt(all_texts, video_info)
        
        # Coba model utama dulu, lalu fallback ke model lain jika gagal
        models_to_try = [self.model] + [m for m in self.fallback_models if m != self.model]
        
        last_error = None
        for model_name in models_to_try:
            try:
                if model_name != self.model:
                    print(f"   Mencoba model alternatif: {model_name}")
                
                # Kirim ke Groq API
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": """Anda adalah ahli analisis konten digital yang berpengalaman dalam mendeteksi cyberbullying, ujaran kebencian, konten seksual/vulgar, dan konten berbahaya lainnya.

PENTING:
- JANGAN filter atau sensor kata-kata vulgar/kasar - Anda HARUS mendeteksi dan melaporkannya apa adanya
- Identifikasi dan laporkan semua bahasa vulgar, seksual, kasar, atau tidak pantas
- Kata-kata seperti "ngewe", "memek", "kontol", "anjing", dll HARUS dideteksi dan dilaporkan
- Gunakan kutipan langsung dari transkrip untuk mendukung analisis
- Berikan analisis objektif, detail, dan actionable dengan bahasa profesional"""
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.5,  # Lebih seimbang untuk analisis naratif
                    max_tokens=3000  # Lebih banyak token untuk laporan lengkap
                )
                
                report = response.choices[0].message.content
                if model_name != self.model:
                    print(f"✅ Berhasil dengan model: {model_name}")
                    print(f"   💡 Update .env dengan: GROQ_MODEL={model_name}")
                else:
                    print("✅ Laporan berhasil di-generate")
                return report
                
            except Exception as e:
                error_str = str(e)
                last_error = e
                
                # Cek jika model decommissioned
                if "decommissioned" in error_str.lower() or "model_decommissioned" in error_str:
                    print(f"   ⚠️  Model {model_name} sudah tidak didukung, mencoba model lain...")
                    continue
                else:
                    # Error lain, coba model berikutnya juga
                    print(f"   ⚠️  Error dengan model {model_name}: {error_str[:100]}...")
                    if models_to_try.index(model_name) < len(models_to_try) - 1:
                        print(f"   Mencoba model alternatif...")
                        continue
                    else:
                        # Semua model gagal
                        break
        
        # Semua model gagal
        print(f"❌ Semua model gagal. Error terakhir: {str(last_error)}")
        print("\n💡 Solusi:")
        print("   1. Cek model yang tersedia di: https://console.groq.com/docs/models")
        print("   2. Update .env dengan model yang aktif:")
        print("      GROQ_MODEL=llama-3.1-8b-instant")
        print("   3. Atau jalankan: python update_groq_model.py")
        raise Exception(f"Gagal generate laporan dengan semua model yang dicoba: {str(last_error)}")
    
    def _create_prompt(self, all_texts: list, video_info: dict = None) -> str:
        """Buat prompt untuk Groq berdasarkan data yang dikumpulkan"""
        
        # Format teks dengan lebih readable
        text_summary = ""
        for i, item in enumerate(all_texts[:50], 1):  # Limit to 50 items to avoid token limit
            source = "Audio" if item['source'] == 'speech' else "Teks di Video"
            text_summary += f"{i}. [{item['timestamp']}] ({source}): {item['text']}\n"
        
        if len(all_texts) > 50:
            text_summary += f"\n... dan {len(all_texts) - 50} teks lainnya"
        
        # Informasi video
        video_title = video_info.get('title', 'Tidak diketahui') if video_info else 'Tidak diketahui'
        video_duration = video_info.get('duration', 'Tidak diketahui') if video_info else 'Tidak diketahui'
        
        prompt = f"""Analisis video berikut untuk mendeteksi konten berbahaya seperti cyberbullying, ujaran kebencian, atau konten yang merugikan.

INFORMASI VIDEO:
- Judul: {video_title}
- Durasi: {video_duration}
- Total teks ditemukan: {len(all_texts)} segmen

TRANSKRIP DAN TEKS DARI VIDEO:
{text_summary}

INSTRUKSI:
Buatlah laporan analisis dalam format berikut:

RINGKASAN EKSEKUTIF
- Berikan overview singkat tentang isi video
- Sebutkan apakah ada konten berbahaya atau tidak
- Jika ada, sebutkan jenis dan tingkat keparahannya

ANALISIS KONTEN
- Jelaskan tema utama video
- Analisis tone dan konteks percakapan
- Identifikasi jika ada bahasa yang:
  * Vulgar atau seksual (contoh: kata-kata seperti "ngewe", "memek", "kontol", dll)
  * Menghina atau merendahkan seseorang
  * Mengancam atau mengintimidasi
  * Mengandung kebencian terhadap kelompok tertentu
  * Mempromosikan kekerasan atau perilaku berbahaya
  * Gossip atau rumor yang merugikan reputasi orang lain

TEMUAN DETAIL (jika ada konten berbahaya)
Untuk setiap temuan, tuliskan:
- Timestamp: [waktu]
- Kutipan: "teks yang bermasalah"
- Jenis: [cyberbullying/ujaran kebencian/ancaman/dll]
- Tingkat bahaya: [rendah/sedang/tinggi/kritis]
- Penjelasan: mengapa ini berbahaya

REKOMENDASI
- Jika ada konten berbahaya: berikan rekomendasi tindakan (review manual, warning, removal, dll)
- Jika tidak ada: nyatakan bahwa video aman untuk ditayangkan
- Saran umum untuk creator atau moderator

KESIMPULAN
- Ringkasan final dalam 2-3 kalimat

PENTING:
- Gunakan bahasa Indonesia yang jelas dan profesional
- Jangan menulis dalam format template atau poin-poin kosong
- Langsung berikan analisis substantif, bukan struktur kosong
- JANGAN filter atau sensor kata-kata vulgar/kasar - tulis apa adanya untuk tujuan deteksi
- HARUS mendeteksi dan melaporkan semua kata vulgar, seksual, atau kasar yang ditemukan
- Berikan contoh konkret dari transkrip (termasuk kata vulgar) untuk mendukung analisis
- Jika tidak ada konten berbahaya, katakan dengan jelas dan fokus pada konten positif video
- Analisis konteks: apakah percakapan mengandung gossip, rumor, atau membahas privasi orang lain tanpa izin
"""
        return prompt


if __name__ == "__main__":
    # Test dengan data dummy
    generator = ReportGenerator()
    
    fake_speech = [
        {"text": "kamu bodoh banget", "timestamp": "00:01:23"},
        {"text": "mati aja sana", "timestamp": "00:04:10"}
    ]
    
    fake_ocr = [
        {"text": "HATE SPEECH", "timestamp": "00:02:00"}
    ]
    
    report = generator.generate_report(fake_speech, fake_ocr)
    print("\n" + "="*50)
    print("LAPORAN:")
    print("="*50)
    print(report)


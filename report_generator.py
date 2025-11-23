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
                            "content": "Kamu adalah ahli analisis konten video yang berpengalaman dalam mendeteksi cyberbullying, ujaran kebencian, dan konten berbahaya lainnya."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2,  # Lebih deterministik untuk laporan
                    max_tokens=2000
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
        
        # Format data menjadi JSON string
        data_json = json.dumps(all_texts, indent=2, ensure_ascii=False)
        
        prompt = f"""
Buatkan laporan analisis cyberbullying dan konten berbahaya dari video berikut.

**Informasi Video:**
{json.dumps(video_info, indent=2, ensure_ascii=False) if video_info else "Tidak tersedia"}

**Data Teks yang Ditemukan:**
{data_json}

**Instruksi:**
Buatkan laporan lengkap yang berisi:

1. **Ringkasan Video**
   - Durasi dan informasi umum
   - Sumber teks (speech-to-text, OCR)

2. **Analisis Konten**
   - Identifikasi jenis konten berbahaya (jika ada):
     * Cyberbullying (penghinaan, ancaman, pelecehan)
     * Ujaran kebencian
     * Konten yang merendahkan
     * Konten yang membahayakan
   - Tingkat bahaya (rendah/sedang/tinggi/sangat tinggi)
   - Dampak potensial

3. **Temuan Detail**
   - List semua temuan dengan timestamp
   - Kutipan teks yang bermasalah
   - Klasifikasi jenis masalah

4. **Rekomendasi**
   - Tindakan yang disarankan
   - Langkah pencegahan
   - Saran untuk moderator/konten creator

**Format Output:**
Gunakan format yang jelas dan terstruktur dengan heading yang jelas.
Gunakan bahasa Indonesia yang profesional dan mudah dipahami.

Mulai generate laporan sekarang:
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


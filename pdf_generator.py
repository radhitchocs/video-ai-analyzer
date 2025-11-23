"""
Modul untuk generate PDF dari laporan teks
"""
try:
    from fpdf import FPDF
except ImportError:
    # Fallback untuk fpdf2
    from fpdf2 import FPDF
from datetime import datetime
import os
import unicodedata


class PDFGenerator:
    def __init__(self):
        """Inisialisasi PDF generator"""
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
    
    def sanitize_text(self, text: str) -> str:
        """
        Bersihkan teks dari karakter Unicode yang tidak didukung oleh font Latin-1
        Konversi karakter fullwidth dan special Unicode ke ASCII equivalent
        """
        if not text:
            return ""
        
        # Mapping karakter fullwidth ke ASCII
        replacements = {
            '：': ':',  # Fullwidth colon
            '｜': '|',  # Fullwidth vertical bar
            '（': '(',  # Fullwidth left parenthesis
            '）': ')',  # Fullwidth right parenthesis
            '，': ',',  # Fullwidth comma
            '。': '.',  # Fullwidth period
            '！': '!',  # Fullwidth exclamation
            '？': '?',  # Fullwidth question mark
            '【': '[',  # Fullwidth left bracket
            '】': ']',  # Fullwidth right bracket
            '「': '"',  # Left corner bracket
            '」': '"',  # Right corner bracket
            '『': '"',  # Double left corner bracket
            '』': '"',  # Double right corner bracket
            '　': ' ',  # Fullwidth space
            '－': '-',  # Fullwidth hyphen
            '～': '~',  # Fullwidth tilde
            '＃': '#',  # Fullwidth hash
        }
        
        # Terapkan replacements
        for fullwidth, ascii_char in replacements.items():
            text = text.replace(fullwidth, ascii_char)
        
        # Normalisasi Unicode (NFKD = compatibility decomposition)
        text = unicodedata.normalize('NFKD', text)
        
        # Hilangkan karakter yang tidak bisa di-encode ke latin-1
        # Coba encode ke latin-1, jika gagal ganti dengan '?'
        cleaned = ''
        for char in text:
            try:
                char.encode('latin-1')
                cleaned += char
            except UnicodeEncodeError:
                # Coba dapatkan ASCII equivalent
                ascii_equiv = unicodedata.normalize('NFKD', char).encode('ascii', 'ignore').decode('ascii')
                if ascii_equiv:
                    cleaned += ascii_equiv
                else:
                    # Jika tidak ada equivalent, skip karakter (atau ganti dengan space jika bukan control char)
                    if not unicodedata.category(char).startswith('C'):
                        cleaned += ' '
        
        return cleaned
    
    def create_report_pdf(self, report_text: str, output_path: str, video_info: dict = None, 
                          speech_data: list = None, ocr_data: list = None):
        """
        Buat PDF dari laporan teks
        
        Args:
            report_text: Teks laporan
            output_path: Path untuk menyimpan PDF
            video_info: Informasi video (opsional)
            speech_data: Data transkrip audio (opsional)
            ocr_data: Data OCR dari video (opsional)
        """
        print(f"📄 Generating PDF: {output_path}")
        
        # Tambahkan halaman pertama
        self.pdf.add_page()
        
        # Header
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, "LAPORAN ANALISIS VIDEO AI", ln=1, align="C")
        
        # Informasi video jika ada
        if video_info:
            self.pdf.set_font("Arial", "", 10)
            self.pdf.ln(5)
            if "title" in video_info:
                title = self.sanitize_text(video_info['title'])
                self.pdf.cell(0, 5, f"Judul: {title}", ln=1)
            if "url" in video_info:
                url = self.sanitize_text(video_info['url'])
                self.pdf.cell(0, 5, f"URL: {url}", ln=1)
        
        # Tanggal dan waktu
        self.pdf.set_font("Arial", "", 10)
        self.pdf.ln(5)
        date_str = datetime.now().strftime("%d %B %Y, %H:%M:%S")
        self.pdf.cell(0, 5, f"Tanggal: {date_str}", ln=1)
        
        # Garis pemisah
        self.pdf.ln(5)
        self.pdf.line(10, self.pdf.get_y(), 200, self.pdf.get_y())
        self.pdf.ln(10)
        
        # Isi laporan
        self.pdf.set_font("Arial", "", 11)
        
        # Split teks menjadi paragraf dan proses
        paragraphs = report_text.split('\n\n')
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Sanitasi text terlebih dahulu
            para = self.sanitize_text(para)
            
            # Cek jika ini heading (baris pendek, biasanya huruf besar atau ada tanda khusus)
            if len(para) < 100 and (para.isupper() or para.startswith('**') or para.startswith('#')):
                # Ini heading
                self.pdf.set_font("Arial", "B", 12)
                # Hapus markdown formatting
                para = para.replace('**', '').replace('#', '').strip()
                self.pdf.cell(0, 8, para, ln=1)
                self.pdf.ln(2)
                self.pdf.set_font("Arial", "", 11)
            else:
                # Ini paragraf biasa
                # Hapus markdown formatting sederhana
                para = para.replace('**', '').replace('*', '').replace('#', '').strip()
                
                # Wrap text untuk PDF
                self.pdf.multi_cell(0, 6, para)
                self.pdf.ln(3)
        
        # Tambahkan section transkrip jika ada
        if speech_data and len(speech_data) > 0:
            self.pdf.add_page()
            
            # Header section transkrip
            self.pdf.set_font("Arial", "B", 14)
            self.pdf.cell(0, 10, "TRANSKRIP LENGKAP", ln=1, align="C")
            self.pdf.ln(5)
            
            # Info jumlah segmen
            self.pdf.set_font("Arial", "I", 10)
            self.pdf.cell(0, 5, f"Total {len(speech_data)} segmen audio", ln=1)
            self.pdf.ln(5)
            
            # Transkrip
            self.pdf.set_font("Arial", "", 10)
            for segment in speech_data:
                timestamp = segment.get("timestamp", "00:00:00")
                text = self.sanitize_text(segment.get("text", ""))
                
                # Format: (timestamp) text
                line = f"({timestamp}) {text}"
                self.pdf.multi_cell(0, 5, line)
                self.pdf.ln(2)
        
        # Tambahkan section OCR jika ada
        if ocr_data and len(ocr_data) > 0:
            self.pdf.add_page()
            
            # Header section OCR
            self.pdf.set_font("Arial", "B", 14)
            self.pdf.cell(0, 10, "TEKS DARI VIDEO (OCR)", ln=1, align="C")
            self.pdf.ln(5)
            
            # Info jumlah frame
            self.pdf.set_font("Arial", "I", 10)
            self.pdf.cell(0, 5, f"Total {len(ocr_data)} frame dengan teks", ln=1)
            self.pdf.ln(5)
            
            # OCR data
            self.pdf.set_font("Arial", "", 10)
            for item in ocr_data:
                timestamp = item.get("timestamp", "00:00:00")
                text = self.sanitize_text(item.get("text", ""))
                
                # Format: [timestamp] text
                line = f"[{timestamp}] {text}"
                self.pdf.multi_cell(0, 5, line)
                self.pdf.ln(2)
        
        # Footer di setiap halaman
        self.pdf.set_auto_page_break(auto=True, margin=15)
        
        # Simpan PDF
        try:
            # Pastikan direktori output ada
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            self.pdf.output(output_path)
            print(f"✅ PDF berhasil dibuat: {output_path}")
        except Exception as e:
            print(f"❌ Error saat membuat PDF: {str(e)}")
            raise


def create_pdf_report(report_text: str, output_path: str, video_info: dict = None,
                     speech_data: list = None, ocr_data: list = None):
    """
    Helper function untuk membuat PDF report
    
    Args:
        report_text: Teks laporan
        output_path: Path untuk menyimpan PDF
        video_info: Informasi video (opsional)
        speech_data: Data transkrip audio (opsional)
        ocr_data: Data OCR dari video (opsional)
    """
    generator = PDFGenerator()
    generator.create_report_pdf(report_text, output_path, video_info, speech_data, ocr_data)


if __name__ == "__main__":
    # Test
    test_report = """
LAPORAN ANALISIS CYBERBULLYING VIDEO

Ringkasan:
Video ini mengandung 2 temuan cyberbullying dengan tingkat bahaya tinggi.

Temuan:
1) 00:01:23 – "kamu bodoh banget"
   - Jenis: penghinaan verbal
   - Tingkat bahaya: sedang

2) 00:04:10 – "mati aja sana"
   - Jenis: ancaman / dorongan bunuh diri
   - Tingkat bahaya: sangat tinggi

Rekomendasi:
- Video perlu direview moderator.
- Pertimbangkan tindakan penghapusan atau pembatasan.
"""
    
    create_pdf_report(test_report, "output/test_report.pdf")


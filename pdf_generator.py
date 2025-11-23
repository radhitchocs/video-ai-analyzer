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


class PDFGenerator:
    def __init__(self):
        """Inisialisasi PDF generator"""
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
    
    def create_report_pdf(self, report_text: str, output_path: str, video_info: dict = None):
        """
        Buat PDF dari laporan teks
        
        Args:
            report_text: Teks laporan
            output_path: Path untuk menyimpan PDF
            video_info: Informasi video (opsional)
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
                self.pdf.cell(0, 5, f"Judul: {video_info['title']}", ln=1)
            if "url" in video_info:
                self.pdf.cell(0, 5, f"URL: {video_info['url']}", ln=1)
        
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


def create_pdf_report(report_text: str, output_path: str, video_info: dict = None):
    """
    Helper function untuk membuat PDF report
    
    Args:
        report_text: Teks laporan
        output_path: Path untuk menyimpan PDF
        video_info: Informasi video (opsional)
    """
    generator = PDFGenerator()
    generator.create_report_pdf(report_text, output_path, video_info)


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


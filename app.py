"""
Streamlit UI untuk Video AI Analyzer - Improved Version
Menggunakan fungsi analyze_video() dari main.py dengan UI yang lebih user-friendly
"""
import os
import sys
import json
import io
import contextlib
from pathlib import Path
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

# Import fungsi dari main.py
from main import analyze_video

# Load environment variables
load_dotenv()

# Konfigurasi halaman
st.set_page_config(
    page_title="Video AI Analyzer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling yang lebih modern
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        text-align: center;
        padding: 2.5rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.95;
        margin-top: 0.5rem;
    }
    
    /* Card Styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border: 1px solid #e0e0e0;
    }
    
    /* Progress Styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Alert Boxes */
    .success-box {
        padding: 1.2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.2);
    }
    
    .error-box {
        padding: 1.2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(220, 53, 69, 0.2);
    }
    
    .warning-box {
        padding: 1.2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(255, 193, 7, 0.2);
    }
    
    /* Process Steps */
    .step-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .step-container:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .step-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
    
    /* Download Button Styling */
    .stDownloadButton > button {
        border-radius: 8px;
        font-weight: 500;
        width: 100%;
    }
    
    /* Metric Styling */
    .metric-container {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Text Area Styling */
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        font-family: 'Courier New', monospace;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    .status-processing {
        background: #fff3cd;
        color: #856404;
    }
    
    .status-success {
        background: #d4edda;
        color: #155724;
    }
    
    .status-error {
        background: #f8d7da;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)


def capture_output(func, *args, **kwargs):
    """
    Menangkap output dari fungsi yang menggunakan print() dan sys.exit()
    Mengembalikan tuple: (output_text, success, error_message)
    """
    output_buffer = io.StringIO()
    error_buffer = io.StringIO()
    
    original_exit = sys.exit
    exit_called = [False]
    exit_code = [0]
    
    def custom_exit(code=0):
        exit_called[0] = True
        exit_code[0] = code
        raise SystemExit(code)
    
    try:
        sys.exit = custom_exit
        
        with contextlib.redirect_stdout(output_buffer), \
             contextlib.redirect_stderr(error_buffer):
            try:
                func(*args, **kwargs)
                success = True
                error_message = None
            except SystemExit:
                success = False
                error_message = "Proses dihentikan karena error"
            except Exception as e:
                success = False
                error_message = str(e)
                import traceback
                error_buffer.write(traceback.format_exc())
            finally:
                sys.exit = original_exit
                
    except Exception as e:
        success = False
        error_message = str(e)
        sys.exit = original_exit
    
    output_text = output_buffer.getvalue()
    error_text = error_buffer.getvalue()
    
    if error_text and not error_message:
        error_message = error_text
    
    if exit_called[0] and exit_code[0] != 0:
        success = False
        if not error_message:
            error_message = f"Proses gagal (exit code: {exit_code[0]})"
    
    return output_text, success, error_message


def get_latest_report_files():
    """Mendapatkan file laporan terbaru dari folder output"""
    output_dir = os.getenv("OUTPUT_DIR", "output")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    files = {
        "txt": None,
        "pdf": None,
        "json": None
    }
    
    if os.path.exists(output_dir):
        for file in sorted(Path(output_dir).glob("report_*"), reverse=True):
            ext = file.suffix[1:].lower()
            if ext in files and files[ext] is None:
                files[ext] = file
    
    return files


def display_process_steps(current_step=0):
    """Menampilkan step-by-step process"""
    steps = [
        {"icon": "📥", "title": "Download Video", "desc": "Mengunduh video dari URL"},
        {"icon": "🎵", "title": "Ekstrak Audio", "desc": "Memisahkan audio dari video"},
        {"icon": "🎤", "title": "Speech-to-Text", "desc": "Transkripsi audio dengan Whisper AI"},
        {"icon": "📸", "title": "OCR Frame", "desc": "Ekstraksi teks dari visual"},
        {"icon": "🤖", "title": "Generate Laporan", "desc": "Analisis dengan Groq AI"}
    ]
    
    cols = st.columns(5)
    for idx, (col, step) in enumerate(zip(cols, steps)):
        with col:
            status = "✅" if idx < current_step else "⏳" if idx == current_step else "⏸️"
            st.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2rem;">{step['icon']}</div>
                    <div style="font-weight: 600; margin: 0.5rem 0;">{step['title']}</div>
                    <div style="font-size: 0.8rem; color: #666;">{step['desc']}</div>
                    <div style="font-size: 1.5rem; margin-top: 0.5rem;">{status}</div>
                </div>
            """, unsafe_allow_html=True)


def main():
    """Main Streamlit app"""
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🎬 Video AI Analyzer</h1>
            <p>Sistem Analisis Video Cerdas untuk Deteksi Cyberbullying dan Konten Berbahaya</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar untuk konfigurasi
    with st.sidebar:
        st.markdown("## ⚙️ Konfigurasi Analisis")
        
        # Input URL video dengan validation
        video_url = st.text_input(
            "📺 URL Video",
            placeholder="https://youtube.com/watch?v=xxxxx",
            help="Masukkan URL video YouTube atau platform video lainnya"
        )
        
        # Validasi URL real-time
        if video_url:
            if video_url.startswith(("http://", "https://")):
                st.success("✅ Format URL valid")
            else:
                st.error("❌ URL harus dimulai dengan http:// atau https://")
        
        # Pilih format output dengan icon
        st.markdown("### 📄 Format Output")
        output_format = st.radio(
            "Pilih format laporan:",
            options=["all", "txt", "pdf", "json"],
            format_func=lambda x: {
                "all": "📦 Semua Format (TXT + PDF + JSON)",
                "txt": "📝 Text File (.txt)",
                "pdf": "📕 PDF Document (.pdf)",
                "json": "📊 JSON Data (.json)"
            }[x],
            help="Pilih format output yang Anda inginkan"
        )
        
        st.markdown("---")
        
        # Fitur dengan expand
        with st.expander("✨ Fitur Utama", expanded=False):
            st.markdown("""
            - ✅ Download video otomatis
            - ✅ Ekstraksi audio berkualitas tinggi
            - ✅ Speech-to-text dengan Whisper AI
            - ✅ OCR dari frame video
            - ✅ Analisis AI dengan Groq
            - ✅ Multi-format export
            - ✅ Deteksi konten berbahaya
            - ✅ Laporan detail dan lengkap
            """)
        
        # System requirements
        with st.expander("ℹ️ Persyaratan Sistem", expanded=False):
            st.markdown("""
            **Pastikan hal berikut:**
            - ✓ Groq API Key sudah di-set
            - ✓ Koneksi internet stabil
            - ✓ Video URL valid dan accessible
            - ✓ Ruang penyimpanan cukup
            """)
        
        # Check API Key
        st.markdown("---")
        st.markdown("### 🔑 Status API")
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            st.success("✅ API Key terdeteksi")
        else:
            st.error("❌ API Key tidak ditemukan")
            st.info("Set GROQ_API_KEY di file .env")
    
    # Main content area
    if not video_url:
        # Welcome screen
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
                <div class="info-card">
                    <h2>🚀 Selamat Datang!</h2>
                    <p>Video AI Analyzer adalah tool canggih untuk menganalisis konten video secara otomatis menggunakan teknologi AI.</p>
                    <br>
                    <h3>Cara Penggunaan:</h3>
                    <ol>
                        <li>Masukkan URL video di sidebar</li>
                        <li>Pilih format output yang diinginkan</li>
                        <li>Klik tombol "Mulai Analisis"</li>
                        <li>Tunggu proses selesai</li>
                        <li>Download laporan hasil analisis</li>
                    </ol>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="feature-card">
                    <h3>📊 Statistik</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Statistik sederhana
            output_dir = os.getenv("OUTPUT_DIR", "output")
            if os.path.exists(output_dir):
                total_reports = len(list(Path(output_dir).glob("report_*")))
                st.metric("Total Laporan", total_reports)
        
        # Tampilkan laporan terbaru
        st.markdown("---")
        st.markdown("## 📁 Laporan Terbaru")
        
        report_files = get_latest_report_files()
        
        if any(report_files.values()):
            tabs = st.tabs(["📝 Text", "📕 PDF", "📊 JSON"])
            
            for idx, (format_type, tab) in enumerate(zip(["txt", "pdf", "json"], tabs)):
                with tab:
                    file_path = report_files[format_type]
                    if file_path and file_path.exists():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.info(f"📄 **{file_path.name}**")
                            st.caption(f"Ukuran: {file_path.stat().st_size / 1024:.2f} KB")
                            st.caption(f"Dibuat: {datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%d %b %Y, %H:%M')}")
                        
                        with col2:
                            with open(file_path, "rb") as f:
                                st.download_button(
                                    label=f"📥 Download",
                                    data=f.read(),
                                    file_name=file_path.name,
                                    mime="application/pdf" if format_type == "pdf" else "application/octet-stream",
                                    key=f"download_{format_type}",
                                    use_container_width=True
                                )
                        
                        # Preview untuk TXT dan JSON
                        if format_type == "txt":
                            with st.expander("👁️ Preview Konten"):
                                with open(file_path, "r", encoding="utf-8") as f:
                                    content = f.read()
                                    st.text_area(
                                        "Isi Laporan",
                                        value=content[:2000] + ("..." if len(content) > 2000 else ""),
                                        height=300,
                                        disabled=True
                                    )
                        
                        elif format_type == "json":
                            with st.expander("👁️ Preview Data"):
                                with open(file_path, "r", encoding="utf-8") as f:
                                    try:
                                        json_data = json.load(f)
                                        st.json(json_data)
                                    except:
                                        st.error("Format JSON tidak valid")
                    else:
                        st.info(f"Belum ada laporan format {format_type.upper()}")
        else:
            st.info("Belum ada laporan yang tersedia. Mulai analisis untuk membuat laporan pertama!")
        
        return
    
    # Validasi URL
    if not video_url.startswith(("http://", "https://")):
        st.error("❌ URL tidak valid. Pastikan URL dimulai dengan http:// atau https://")
        return
    
    # Area untuk tombol analisis
    st.markdown("## 🎯 Mulai Analisis Video")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start_button = st.button(
            "🚀 Mulai Analisis",
            type="primary",
            use_container_width=True
        )
    
    if start_button:
        # Container untuk hasil
        result_container = st.container()
        
        with result_container:
            # Display steps
            st.markdown("### 📋 Proses Analisis")
            steps_placeholder = st.empty()
            
            with steps_placeholder.container():
                display_process_steps(0)
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Log container
            with st.expander("📊 Live Log", expanded=True):
                log_placeholder = st.empty()
            
            # Simulasi step-by-step (akan diganti dengan real progress)
            steps_info = [
                (10, "📥 Mendownload video...", 1),
                (30, "🎵 Mengekstrak audio...", 2),
                (50, "🎤 Melakukan transkripsi...", 3),
                (70, "📸 Mengekstrak teks dari frame...", 4),
                (90, "🤖 Menghasilkan laporan AI...", 5)
            ]
            
            # Jalankan analisis
            try:
                output_text, success, error_message = capture_output(
                    analyze_video,
                    video_url,
                    output_format
                )
                
                progress_bar.progress(100)
                steps_placeholder.empty()
                
                if success:
                    with steps_placeholder.container():
                        display_process_steps(6)
                    
                    status_text.markdown("""
                        <div class="success-box">
                            <h3>✅ Analisis Berhasil Diselesaikan!</h3>
                            <p>Laporan telah berhasil dibuat dan siap diunduh.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Show log
                    with log_placeholder.container():
                        st.text_area(
                            "Log Proses",
                            value=output_text,
                            height=200,
                            disabled=True
                        )
                    
                    # Tampilkan file hasil
                    st.markdown("---")
                    st.markdown("## 📁 Hasil Analisis")
                    
                    report_files = get_latest_report_files()
                    
                    tabs = st.tabs(["📝 Text", "📕 PDF", "📊 JSON"])
                    
                    for idx, (format_type, tab) in enumerate(zip(["txt", "pdf", "json"], tabs)):
                        with tab:
                            file_path = report_files[format_type]
                            if file_path and file_path.exists():
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.success(f"✅ File {format_type.upper()} berhasil dibuat!")
                                    st.info(f"📄 **{file_path.name}**")
                                    st.caption(f"Ukuran: {file_path.stat().st_size / 1024:.2f} KB")
                                
                                with col2:
                                    with open(file_path, "rb") as f:
                                        st.download_button(
                                            label=f"📥 Download {format_type.upper()}",
                                            data=f.read(),
                                            file_name=file_path.name,
                                            mime="application/pdf" if format_type == "pdf" else "application/octet-stream",
                                            key=f"result_download_{format_type}",
                                            use_container_width=True
                                        )
                                
                                # Preview
                                if format_type == "txt":
                                    with st.expander("👁️ Preview Laporan"):
                                        with open(file_path, "r", encoding="utf-8") as f:
                                            content = f.read()
                                            st.text_area(
                                                "Isi Lengkap",
                                                value=content,
                                                height=400,
                                                disabled=True
                                            )
                                
                                elif format_type == "json":
                                    with st.expander("👁️ Preview Data JSON"):
                                        with open(file_path, "r", encoding="utf-8") as f:
                                            try:
                                                json_data = json.load(f)
                                                st.json(json_data)
                                            except:
                                                st.error("Format JSON tidak valid")
                            else:
                                if output_format == "all" or output_format == format_type:
                                    st.warning(f"⚠️ File {format_type.upper()} tidak ditemukan")
                                else:
                                    st.info(f"ℹ️ Format {format_type.upper()} tidak dipilih")
                    
                    # Success message dengan confetti
                    st.balloons()
                    
                else:
                    status_text.markdown(f"""
                        <div class="error-box">
                            <h3>❌ Analisis Gagal</h3>
                            <p><strong>Error:</strong> {error_message}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if output_text:
                        with log_placeholder.container():
                            st.text_area(
                                "Log Error",
                                value=output_text,
                                height=300,
                                disabled=True
                            )
            
            except Exception as e:
                progress_bar.progress(100)
                status_text.markdown(f"""
                    <div class="error-box">
                        <h3>❌ Terjadi Kesalahan</h3>
                        <p><strong>Error:</strong> {str(e)}</p>
                    </div>
                """, unsafe_allow_html=True)
                st.exception(e)


if __name__ == "__main__":
    main()

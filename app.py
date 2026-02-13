import streamlit as st
import base64
from pathlib import Path

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Iftanul Ibnu | Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. FUNGSI LOAD GAMBAR (Supaya Aman)
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return None

# Load Foto
img_path = "assets/profile.jpg"
img_base64 = get_base64_image(img_path)

# 3. CSS "NUCLEAR" (PENYELESAIAN MASALAH VISUAL)
st.markdown("""
    <style>
    /* --- PERBAIKAN PANAH SIDEBAR (FORCE WHITE) --- */
    /* Kita targetkan path SVG-nya langsung agar warnanya putih */
    [data-testid="stSidebarCollapseButton"] > span > svg > path {
        fill: white !important;
        stroke: white !important;
    }
    /* Backup selector jika struktur browser beda */
    button[kind="header"] svg path {
        fill: white !important;
        stroke: white !important;
    }

    /* --- BACKGROUND GELAP (GREY THEME) --- */
    .stApp {
        background-color: #1A1A1A;
        color: white;
    }
    
    /* Header Transparan */
    [data-testid="stHeader"] {
        background-color: transparent;
    }

    /* Sidebar Gelap */
    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #333;
    }
    
    /* Teks Navigasi Sidebar */
    [data-testid="stSidebarNavItems"] span {
        color: #E0E0E0 !important;
    }

    /* --- TOMBOL UTAMA --- */
    .stButton > button {
        background-color: #9EE05B !important; /* Hijau Neon */
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: white !important;
        transform: scale(1.05);
    }

    /* --- FOTO PROFIL (HTML MURNI) --- */
    /* Ini style untuk tag <img> HTML, bukan st.image */
    .profile-img-html {
        width: 350px;
        height: 350px;
        object-fit: cover;        /* Memotong gambar agar pas frame */
        object-position: top;     /* Fokus ke wajah bagian atas */
        border-radius: 50%;       /* Membuat lingkaran */
        border: 5px solid #9EE05B;
        display: block;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0px 0px 20px rgba(158, 224, 91, 0.3);
    }
    
    /* Typography */
    .main-title { font-size: 4rem; font-weight: 800; line-height: 1.2; color: white; }
    .highlight { color: #9EE05B; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR (KOSONGKAN AGAR BERSIH)
with st.sidebar:
    st.write("") 

# 5. LAYOUT UTAMA
st.write("##") # Spacer atas

col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.5rem; color:#CCC; margin-bottom:0;">Hi, I\'m Ibnu</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">I\'m <span class="highlight">Data Science</span> & Data Analyst.</h1>', unsafe_allow_html=True)
    
    st.markdown('''
        <p style="font-size: 1.2rem; color: #BBB; line-height: 1.6;">
        Membantu bisnis mengambil keputusan berbasis data melalui 
        Machine Learning, Predictive Analytics, dan Visualisasi yang efektif.
        </p>
    ''', unsafe_allow_html=True)
    
    st.write("##")
    
    # --- LOGIKA TOMBOL PINDAH HALAMAN ---
    if st.button("Lihat Project Saya ➔"):
        # Cek apakah file tujuannya benar-benar ada
        project_file = Path("pages/2_Projects.py")
        if project_file.is_file():
            st.switch_page("pages/2_Projects.py")
        else:
            st.error("⚠️ Error: File 'pages/2_Projects.py' tidak ditemukan!")
            st.info("Pastikan kamu punya folder bernama 'pages' (huruf kecil) dan file '2_Projects.py' di dalamnya.")

with col2:
    # --- CARA RENDER GAMBAR AGAR BULAT SEMPURNA (HTML) ---
    if img_base64:
        st.markdown(
            f'<img src="data:image/png;base64,{img_base64}" class="profile-img-html">',
            unsafe_allow_html=True
        )
    else:
        # Placeholder jika gambar rusak/tidak ada
        st.markdown("""
            <div style="width:350px; height:350px; border-radius:50%; border:5px dashed #9EE05B; 
            display:flex; align-items:center; justify-content:center; color:#9EE05B; margin:auto;">
                <p style="text-align:center;">Foto tidak ditemukan<br>Cek folder assets/</p>
            </div>
        """, unsafe_allow_html=True)

# 6. FOOTER
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("<p style='text-align: center; color: #555;'>© 2026 Ibnu Portfolio. Powered by Streamlit</p>", unsafe_allow_html=True)
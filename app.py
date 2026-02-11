import streamlit as st
import base64

# 1. Halaman
st.set_page_config(
    page_title="Iftanul Ibnu | Data Science Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Load gambar base64
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None

# Load foto profil
img_path = "assets/profile.jpg"
img_base64 = get_base64(img_path)

# 3. Custom CSS
st.markdown(f"""
    <style>
    /* --- MENGATASI PANAH SIDEBAR YANG TIDAK TERLIHAT --- */
    /* Mengubah warna panah sidebar menjadi Putih Terang */
    [data-testid="stSidebarCollapseButton"] svg {{
        fill: white !important;
        stroke: white !important;
        width: 30px;
        height: 30px;
        transition: 0.3s;
    }}
    
    /* Memberi efek glow hijau saat panah di-hover */
    [data-testid="stSidebarCollapseButton"]:hover svg {{
        fill: #9EE05B !important;
        filter: drop-shadow(0px 0px 8px #9EE05B);
    }}

    /* Menghilangkan header putih bawaan Streamlit */
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
    }}
    
    /* Background utama hitam */
    .stApp {{
        background-color: #0E1117;
        color: white;
    }}

    /* Sidebar Gelap */
    [data-testid="stSidebar"] {{
        background-color: #161B22;
        border-right: 1px solid #30363d;
    }}
    
    /* Warna teks menu navigasi otomatis */
    [data-testid="stSidebarNavItems"] span {{
        color: white !important;
        font-weight: 500;
    }}

    /* --- STYLING KONTEN UTAMA --- */
    .main-title {{
        font-size: 4.2rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 20px;
        color: white;
    }}

    .highlight {{
        color: #9EE05B;
    }}

    .sub-title {{
        font-size: 1.2rem;
        color: #B0B0B0;
        max-width: 550px;
        line-height: 1.6;
        margin-bottom: 40px;
    }}

    /* Styling Tombol Hijau */
    .stButton>button {{
        background-color: #9EE05B;
        color: #000000 !important;
        font-weight: 700;
        border-radius: 10px;
        border: none;
        padding: 0.8rem 2.5rem;
        font-size: 1.1rem;
        transition: 0.4s;
    }}
    
    .stButton>button:hover {{
        background-color: #ffffff;
        transform: translateY(-5px);
    }}

    /* FOTO PROFIL */
    .img-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }}

    .profile-pic {{
        width: 380px;
        height: 380px;
        object-fit: cover;
        object-position: center;
        border-radius: 50%;
        border: 6px solid #9EE05B;
        display: block;
        margin: auto:
        padding: 0;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.write("")

# 5. MAIN LAYOUT
st.write("##")

col1, col2 = st.columns([1.3, 1], gap="large")

with col1:
    st.write("###") 
    st.markdown('<p style="font-size: 1.5rem; font-weight: 400; margin-bottom: 0;">Hi, I\'m Ibnu</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">I\'m <span class="highlight">Data Science</span> & Data Analyst.</h1>', unsafe_allow_html=True)
    
    st.markdown('''
        <p class="sub-title">
        Saya adalah Data Scientist yang berfokus pada analisis data dan machine learning untuk menghasilkan insight
        yang berdampak pada pengambilan keputusan.
        </p>
    ''', unsafe_allow_html=True)
    
    if st.button("My Projects ➔"):
        st.switch_page("pages/2_Projects.py")

with col2:
    if img_base64:
        st.markdown(f'''
            <div class="img-container">
                <img src="data:image/png;base64,{img_base64}" class="profile-pic">
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            <div class="img-container">
                <div style="width:380px; height:380px; border-radius:50%; border:6px solid #9EE05B; 
                display:flex; align-items:center; justify-content:center; color:#9EE05B;">
                    <p style="text-align:center;">profile.jpg not found</p>
                </div>
            </div>
        ''', unsafe_allow_html=True)

# 6. FOOTER
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("<p style='text-align: center; color: #555;'>© 2026 Ibnu. Built with Python & Streamlit</p>", unsafe_allow_html=True)
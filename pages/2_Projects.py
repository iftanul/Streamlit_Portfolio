import streamlit as st

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Projects Gallery | Ibnu Portfolio", 
    page_icon="📂", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS STYLING (SIDEBAR GELAP & TEKS PUTIH) ---
st.markdown("""
    <style>
    /* 1. BACKGROUND UTAMA & HEADER (GELAP) */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #1A1A1A !important;
        color: white !important;
    }

    /* 2. SIDEBAR (BACKGROUND GELAP) */
    [data-testid="stSidebar"] {
        background-color: #111111 !important; /* Hitam Premium */
        border-right: 1px solid #333;         /* Garis pemisah tipis */
    }
    
    /* 3. TEKS MENU SIDEBAR (JADI PUTIH) */
    /* Ini yang membuat tulisan 'About Me', 'Projects' jadi Putih */
    [data-testid="stSidebarNav"] span,
    [data-testid="stSidebarNav"] p {
        color: #FFFFFF !important;
        font-weight: 500;
    }
    
    /* Ikon Panah Sidebar juga Putih */
    [data-testid="stSidebarCollapseButton"] svg {
        fill: white !important;
        stroke: white !important;
    }

    /* 4. TOMBOL KEREN */
    /* Keadaan Normal (Hijau Neon) */
    .stButton button {
        background-color: #9EE05B !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: 2px solid #9EE05B !important;
        transition: all 0.3s ease !important;
    }

    /* Keadaan Hover (Abu Soft - Tidak Terlalu Putih Silau) */
    .stButton button:hover {
        background-color: #CCCCCC !important; /* Abu-abu Terang */
        color: black !important;
        border: 2px solid #CCCCCC !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(255, 255, 255, 0.1) !important;
    }

    /* Tombol Disabled (Coming Soon) */
    button:disabled {
        background-color: #333 !important;
        color: #666 !important;
        border: 1px solid #444 !important;
        cursor: not-allowed;
    }

    /* 5. CARD STYLING */
    div.project-card {
        background-color: #252525;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.3s ease;
    }
    div.project-card:hover {
        transform: translateY(-5px);
        border-color: #9EE05B;
        box-shadow: 0 10px 20px rgba(158, 224, 91, 0.1);
    }
    
    /* 6. TYPOGRAPHY */
    .card-title { font-size: 1.2rem; font-weight: 700; color: white; margin-bottom: 5px; }
    .card-category { font-size: 0.8rem; color: #9EE05B; font-weight: 600; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 1px; }
    .card-desc { font-size: 0.9rem; color: #B0B0B0; line-height: 1.5; margin-bottom: 20px; }
    
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT (ROUTER) ---
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'gallery'

def set_view(view_name):
    st.session_state.current_view = view_name

# --- 4. DATA STRUKTUR PROJECT ---
# Ini adalah "Database" mini untuk mengatur isi kartu
projects = [
    {
        "id": "bank_churn",
        "title": "Bank Customer Churn",
        "category": "Classification",
        "desc": "Early Warning System berbasis AI untuk memprediksi nasabah yang berisiko berhenti berlangganan (Churn) dan strategi retensi.",
        "status": "Active",
        "icon": "🏦"
    },
    {
        "id": "nlp_sentiment",
        "title": "Sentiment Analysis (NLP)",
        "category": "Natural Language Processing",
        "desc": "Analisis sentimen ulasan pelanggan (Positif/Negatif) menggunakan Deep Learning / BERT untuk memantau reputasi brand.",
        "status": "Coming Soon",
        "icon": "💬"
    },
    {
        "id": "recsys",
        "title": "Product Recommender",
        "category": "Recommendation System",
        "desc": "Sistem rekomendasi personalisasi (Collaborative Filtering) untuk meningkatkan cross-selling produk e-commerce.",
        "status": "Coming Soon",
        "icon": "🛍️"
    },
    {
        "id": "forecasting",
        "title": "Sales Forecasting",
        "category": "Time Series",
        "desc": "Peramalan penjualan masa depan untuk optimalisasi stok gudang menggunakan SARIMA dan Prophet.",
        "status": "Coming Soon",
        "icon": "📈"
    },
    {
        "id": "rfm",
        "title": "Customer Segmentation",
        "category": "RFM Analysis",
        "desc": "Dashboard segmentasi pelanggan (Loyal, Hibernating, at Risk) tanpa model prediksi, fokus pada visualisasi data bisnis.",
        "status": "Coming Soon",
        "icon": "👥"
    },
    {
        "id": "ab_testing",
        "title": "Marketing A/B Testing",
        "category": "Statistical Inference",
        "desc": "Analisis dampak kampanye marketing (Control vs Treatment) menggunakan uji statistik hipotesis yang ketat.",
        "status": "Coming Soon",
        "icon": "AB"
    },
    {
        "id": "coming_soon",
        "title": "Next Big Project",
        "category": "Experimental",
        "desc": "Proyek inovatif berikutnya sedang dalam tahap riset dan pengembangan.",
        "status": "Coming Soon",
        "icon": "🚀"
    }
]

# --- 5. RENDER GALLERY FUNCTION ---
def render_gallery():
    st.markdown("# 📂 Project <span style='color:#9EE05B'>Gallery</span>", unsafe_allow_html=True)
    st.write("Kumpulan portofolio Data Science yang mencakup berbagai domain: Classification, NLP, Time Series, hingga Analytics.")
    st.write("---")
    
    # Grid Layout: Kita buat 3 kolom per baris
    cols = st.columns(3)
    
    for i, project in enumerate(projects):
        with cols[i % 3]: # Logika agar kartu mengisi kolom 1, 2, 3 lalu pindah baris
            # HTML Card
            st.markdown(f"""
            <div class="project-card">
                <div>
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">{project['icon']}</div>
                    <div class="card-category">{project['category']}</div>
                    <div class="card-title">{project['title']}</div>
                    <div class="card-desc">{project['desc']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Button Logic
            if project['status'] == "Active":
                # Gunakan CSS class btn-active agar hijau
                st.markdown('<div class="btn-active">', unsafe_allow_html=True)
                st.button(f"🚀 Lihat Studi Kasus", key=f"btn_{project['id']}", on_click=set_view, args=(project['id'],))
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                # Gunakan CSS class btn-disabled agar abu-abu
                st.markdown('<div class="btn-disabled">', unsafe_allow_html=True)
                st.button(f"🚧 {project['status']}", key=f"btn_{project['id']}", disabled=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.write("##") # Spacer antar baris grid

# --- 6. MAIN CONTROLLER (THE ROUTER) ---

if st.session_state.current_view == 'gallery':
    render_gallery()

elif st.session_state.current_view == 'bank_churn':
    # --- LOAD PROJECT 1: BANK CHURN ---
    from projects.bank_churn import view as churn_view
    # Jalankan view, dan berikan fungsi 'set_view' agar tombol Back bisa bekerja
    churn_view.run(back_callback=lambda: set_view('gallery'))

# --- TEMPAT UNTUK PROJECT MASA DEPAN (Contoh Struktur) ---
# elif st.session_state.current_view == 'nlp_sentiment':
#     from projects.nlp_sentiment import view as nlp_view
#     nlp_view.run(back_callback=lambda: set_view('gallery'))
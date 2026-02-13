import streamlit as st
import pandas as pd
import pickle
import os

# --- FUNGSI LOAD MODEL ---
def load_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'churn_pipeline.pkl')
    try:
        with open(model_path, 'rb') as file:
            return pickle.load(file)
    except:
        return None

def run(back_callback):
    # Header & Navigasi
    col_a, col_b = st.columns([1, 6])
    with col_a:
        if st.button("⬅️ Back", use_container_width=True):
            back_callback()
            st.rerun()
    with col_b:
        st.caption("Project / Bank Customer Churn")

    st.markdown("# 🏦 Bank Customer Churn Prediction")
    
    tab1, tab2, tab3, tab4 = st.tabs(["💼 Business Case", "📊 EDA", "🤖 Model", "🔮 Simulator"])
    
    with tab4:
        st.markdown("### 🔮 Live Simulator")
        pipeline = load_model()
        
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Profil Nasabah**")
                gender = st.selectbox("Gender", ["M", "F"])
                marital = st.selectbox("Marital Status", ["Married", "Single", "Divorced", "Unknown"])
                # Input angka asli untuk dihitung kategorinya secara otomatis
                age = st.number_input("Age (Input angka)", 18, 100, 45)
                tenure = st.number_input("Tenure (Bulan)", 0, 100, 36)
                education = st.selectbox("Education", ["High School", "College", "Graduate", "Doctorate", "Uneducated", "Post-Graduate", "Unknown"])
                
            with c2:
                st.markdown("**Detail Produk & Transaksi**")
                income = st.selectbox("Income Category", ["Less than $40K", "$40K - $60K", "$60K - $80K", "$80K - $120K", "$120K +", "Unknown"])
                card = st.selectbox("Card Category", ["Blue", "Silver", "Gold", "Platinum"])
                products = st.slider("Total Relationship Count", 1, 6, 3)
                contacts = st.slider("Contacts Count (12 mon)", 0, 12, 2)
                revolving = st.number_input("Total Revolving Bal", 0, 5000, 1000)

            st.markdown("**Rasio Aktivitas**")
            c3, c4, c5 = st.columns(3)
            with c3:
                amt_chng = st.number_input("Amt Chng Q4-Q1", 0.0, 5.0, 0.7)
            with c4:
                ct_chng = st.number_input("Ct Chng Q4-Q1", 0.0, 5.0, 0.6)
            with c5:
                util_ratio = st.slider("Utilization Ratio", 0.0, 1.0, 0.2)

            btn = st.button("🔍 Prediksi Status Nasabah", use_container_width=True)

        if btn:
            if pipeline:
                try:
                    # --- PRE-PROCESSING SESUAI KODE TRAINING ---
                    
                    # 1. Clean Education Level (Sesuai Bagian 2 di kodemu)
                    clean_edu = "Unknown" if education in ["Uneducated", "Post-Graduate"] else education
                    
                    # 2. Logic Age Group (Sesuai Ordinal Encoder di kodemu)
                    if age < 30: age_group = "Young"
                    elif age < 50: age_group = "Adult"
                    else: age_group = "Senior"
                    
                    # 3. Logic Tenure Segment (Sesuai Ordinal Encoder di kodemu)
                    if tenure < 24: tenure_segment = "New"
                    elif tenure < 48: tenure_segment = "Mid"
                    else: tenure_segment = "Long"

                    # 4. Memasukkan data SESUAI URUTAN FITUR yang tersisa di X_train
                    raw_data = {
                        'gender': gender,
                        'dependent_count': 2, # Nilai default karena tidak ada di input
                        'education_level': clean_edu,
                        'marital_status': marital,
                        'income_category': income,
                        'card_category': card,
                        'months_on_book': float(tenure),
                        'total_relationship_count': float(products),
                        'contacts_count_12_mon': float(contacts),
                        'total_revolving_bal': float(revolving),
                        'total_amt_chng_q4_q1': float(amt_chng),
                        'total_ct_chng_q4_q1': float(ct_chng),
                        'avg_utilization_ratio': float(util_ratio),
                        'age_group': age_group,
                        'tenure_segment': tenure_segment
                    }
                    
                    input_df = pd.DataFrame([raw_data])
                    
                    # PREDIKSI 0 atau 1
                    result = pipeline.predict(input_df)[0]
                    
                    st.divider()
                    if result == 1:
                        st.error("🚨 HASIL PREDIKSI: **ATTRITED CUSTOMER (1)**")
                        st.write("Nasabah ini diprediksi akan berhenti menggunakan layanan.")
                    else:
                        st.success("✅ HASIL PREDIKSI: **EXISTING CUSTOMER (0)**")
                        st.write("Nasabah ini diprediksi akan tetap setia.")
                        
                except Exception as e:
                    st.error(f"⚠️ Terjadi kesalahan: {e}")
            else:
                st.error("❌ Model (.pkl) tidak dapat ditemukan.")
import streamlit as st
import pandas as pd
import pickle
import os
import sklearn
import xgboost

# --- FUNGSI LOAD MODEL DENGAN DIAGNOSA LENGKAP ---
def load_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'churn_pipeline.pkl')
    
    # --- DIAGNOSA 1: Cek Versi Library ---
    st.write("--- 🏥 DIAGNOSTIC MODE ---")
    st.write(f"🐍 Python Runtime: {st.secrets.get('python_version', 'Unknown')}")
    st.write(f"📦 Scikit-learn Version: {sklearn.__version__}")
    st.write(f"📦 XGBoost Version: {xgboost.__version__}")
    
    # --- DIAGNOSA 2: Cek Fisik File ---
    if os.path.exists(model_path):
        file_size = os.path.getsize(model_path)
        st.write(f"📂 File Model Ditemukan!")
        st.write(f"📏 Ukuran File: {file_size} bytes ({file_size/1024:.2f} KB)")
        
        # Cek apakah ini file Git LFS (Rusak)
        if file_size < 2000: # Jika kurang dari 2KB, curiga ini cuma pointer
            st.error("🚨 UKURAN FILE TERLALU KECIL! Kemungkinan file model rusak saat upload ke GitHub (Git LFS Pointer).")
            st.info("Solusi: Hapus file .pkl di GitHub, lalu upload ulang menggunakan 'Add file' > 'Upload files' di website GitHub langsung.")
            return None
    else:
        st.error(f"❌ File tidak ditemukan di: {model_path}")
        return None

    # --- DIAGNOSA 3: Coba Load ---
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
            st.success("✅ Model Berhasil Dimuat! (Versi Cocok)")
            return model
    except Exception as e:
        st.error(f"💀 Gagal Load Pickle: {e}")
        return None

# --- FUNGSI UTAMA VIEW ---
def run(back_callback):
    # Header
    c1, c2 = st.columns([1, 6])
    with c1:
        if st.button("⬅️ Back"):
            back_callback()
            st.rerun()
    with c2:
        st.markdown("## 🏥 Debugging Mode: Bank Churn")

    # Jalankan Diagnosa
    pipeline = load_model()

    # Jika model berhasil load, tampilkan form simulator (singkat saja untuk tes)
    if pipeline:
        st.divider()
        st.subheader("🔮 Simulator Test")
        
        # Input Dummy Cepat
        with st.form("quick_test"):
            tenure = st.slider("Tenure", 0, 60, 36)
            trans_ct = st.number_input("Total Transaksi", 0, 150, 40)
            submitted = st.form_submit_button("Test Predict")
            
        if submitted:
            try:
                # Data Dummy
                dummy_df = pd.DataFrame([{
                    'Customer_Age': 45, 'Gender': 'M', 'Dependent_count': 2,
                    'Education_Level': 'Graduate', 'Marital_Status': 'Married',
                    'Income_Category': '$60K - $80K', 'Card_Category': 'Blue',
                    'Months_on_book': tenure, 'Total_Relationship_Count': 3,
                    'Months_Inactive_12_mon': 2, 'Contacts_Count_12_mon': 2,
                    'Credit_Limit': 10000, 'Total_Revolving_Bal': 1000,
                    'Avg_Open_To_Buy': 9000, 'Total_Amt_Chng_Q4_Q1': 0.7,
                    'Total_Trans_Amt': 4000, 'Total_Trans_Ct': trans_ct,
                    'Total_Ct_Chng_Q4_Q1': 0.6, 'Avg_Utilization_Ratio': 0.1
                }])
                dummy_df.columns = [x.lower() for x in dummy_df.columns]
                prob = pipeline.predict_proba(dummy_df)[0][1]
                st.success(f"Prediction Success: {prob:.2%}")
            except Exception as e:
                st.error(f"Prediction Error: {e}")
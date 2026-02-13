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
    except Exception as e:
        # Jika gagal load, return None agar tidak crash
        return None

# --- FUNGSI UTAMA VIEW ---
def run(back_callback):
    # HEADER & NAVIGASI
    col_a, col_b = st.columns([1, 6])
    with col_a:
        if st.button("⬅️ Back", use_container_width=True):
            back_callback()
            st.rerun()
    with col_b:
        st.caption("Project / Bank Customer Churn")

    st.markdown("# 🏦 Bank Customer Churn Prediction")
    
    # TABS
    tab1, tab2, tab3, tab4 = st.tabs([
        "💼 Business Case", "📊 EDA & Insights", "🤖 Model Performance", "🔮 Live Simulator"
    ])
    
    # --- ISI TAB 1-3 (Summary) ---
    with tab1:
        st.info("ℹ️ Buka Tab 'Live Simulator' untuk mencoba prediksi.")
        st.markdown("### 📌 Executive Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("Acquisition Cost", "5x Higher", delta_color="inverse")
        c2.metric("Profit Impact", "+25-95%")
        c3.metric("Current Strategy", "Reactive", delta_color="inverse")

    with tab2:
        st.write("### 🔎 Key Data Insights")
        st.bar_chart(pd.DataFrame({'Importance': [0.85, 0.65, 0.15]}, index=['Transaction', 'Inactive', 'Gender']))

    with tab3:
        st.write("### 🤖 XGBoost Model Evaluation")
        m1, m2, m3 = st.columns(3)
        m1.metric("Accuracy", "94%")
        m2.metric("Recall", "77%")
        m3.metric("ROC AUC", "0.96")

    # --- TAB 4: SIMULATOR ---
    with tab4:
        st.markdown("### 🔮 Prediction Simulator")
        st.write("Masukkan profil nasabah untuk memprediksi risiko churn.")
        
        pipeline = load_model()
        
        # --- INPUT FORM ---
        with st.container(border=True):
            c_in1, c_in2, c_in3 = st.columns(3)
            with c_in1:
                gender = st.selectbox("Gender", ["M", "F"])
                age_grp = st.selectbox("Age Group", ["Young", "Adult", "Senior"])
                marital = st.selectbox("Marital Status", ["Married", "Single", "Divorced", "Unknown"])
                tenure = st.slider("Tenure (Bulan)", 0, 60, 36)
            with c_in2:
                products = st.slider("Total Produk", 1, 6, 2)
                inactive = st.slider("Bulan Inaktif (12 bln)", 0, 12, 1)
                contacts = st.slider("Jumlah Komplain", 0, 6, 2)
                card = st.selectbox("Tipe Kartu", ["Blue", "Silver", "Gold", "Platinum"])
            with c_in3:
                trans_ct = st.number_input("Total Transaksi", 0, 150, 40)
                trans_amt = st.number_input("Nominal Transaksi ($)", 0, 20000, 2000)
                revolving = st.number_input("Saldo Kredit ($)", 0, 3000, 1000)
                util_ratio = st.slider("Utilisasi Limit", 0.0, 1.0, 0.1)

            predict_btn = st.button("🔍 Cek Risiko Churn", use_container_width=True)

        # --- LOGIKA PREDIKSI ---
        if predict_btn:
            churn_prob = 0.0
            prediction_success = False

            # 1. Coba Pakai Model Asli
            if pipeline:
                try:
                    # Buat DataFrame sesuai format model
                    input_df = pd.DataFrame([{
                        'Customer_Age': 45, 'Gender': gender, 'Dependent_count': 2,
                        'Education_Level': 'Graduate', 'Marital_Status': marital,
                        'Income_Category': '$60K - $80K', 'Card_Category': card,
                        'Months_on_book': tenure, 'Total_Relationship_Count': products,
                        'Months_Inactive_12_mon': inactive, 'Contacts_Count_12_mon': contacts,
                        'Credit_Limit': 10000, 'Total_Revolving_Bal': revolving,
                        'Avg_Open_To_Buy': 9000, 'Total_Amt_Chng_Q4_Q1': 0.7,
                        'Total_Trans_Amt': trans_amt, 'Total_Trans_Ct': trans_ct,
                        'Total_Ct_Chng_Q4_Q1': 0.6, 'Avg_Utilization_Ratio': util_ratio
                    }])
                    input_df.columns = [x.lower() for x in input_df.columns]
                    
                    churn_prob = pipeline.predict_proba(input_df)[0][1]
                    prediction_success = True
                except:
                    prediction_success = False

            # 2. Fallback ke Logika Bisnis (Jika model gagal/loading)
            # Ini PENTING agar user tidak melihat error page jika ada masalah teknis
            if not prediction_success:
                base_score = 0.10
                if trans_ct < 40: base_score += 0.35
                if inactive > 2: base_score += 0.25
                if revolving < 500: base_score += 0.15
                if contacts > 3: base_score += 0.10
                churn_prob = min(base_score, 0.98)

            # --- TAMPILAN HASIL ---
            st.divider()
            col_res1, col_res2 = st.columns([1, 2])
            
            with col_res1:
                if churn_prob > 0.5:
                    st.error("HIGH RISK (CHURN)")
                    st.metric("Probability", f"{churn_prob*100:.1f}%")
                else:
                    st.success("LOW RISK (AMAN)")
                    st.metric("Probability", f"{churn_prob*100:.1f}%")
                
                if not prediction_success:
                    st.caption("⚠️ *Menggunakan Simulasi Logika (Model Loading Issue)*")

            with col_res2:
                st.info("💡 **Rekomendasi Strategis:**")
                if churn_prob > 0.7:
                    st.write("🚨 **Urgent:** Segera hubungi nasabah! Tawarkan insentif (Cashback/Diskon).")
                elif churn_prob > 0.4:
                    st.write("⚠️ **Waspada:** Kirim email marketing personalisasi. Pantau transaksi.")
                else:
                    st.write("✅ **Pertahankan:** Tawarkan produk cross-selling.")
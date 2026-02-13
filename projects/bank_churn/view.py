import streamlit as st
import pandas as pd
import pickle
import os

# --- FUNGSI LOAD MODEL ---
def load_model():
    # Mendapatkan path absolut dari file ini
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Path ke file model (pastikan nama file di folder sama persis: churn_pipeline.pkl)
    model_path = os.path.join(current_dir, 'churn_pipeline.pkl')
    
    try:
        with open(model_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        st.error(f"❌ File model tidak ditemukan di: {model_path}")
        return None
    except Exception as e:
        # Tampilkan error asli jika model gagal dimuat (Jujur)
        st.error(f"❌ Error saat memuat model: {e}")
        return None

# --- FUNGSI UTAMA VIEW ---
def run(back_callback):
    # --- HEADER ---
    col_a, col_b = st.columns([1, 6])
    with col_a:
        if st.button("⬅️ Back", use_container_width=True):
            back_callback()
            st.rerun()
    with col_b:
        st.caption("Project / Bank Customer Churn")

    st.markdown("# 🏦 Bank Customer Churn Prediction")
    
    # --- TABS ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "💼 Business Case", 
        "📊 EDA & Insights", 
        "🤖 Model Performance", 
        "🔮 Live Simulator"
    ])
    
    # --- ISI TAB 1-3 (Standar) ---
    with tab1:
        st.info("ℹ️ Masuk ke Tab 'Live Simulator' untuk mencoba model prediksi.")
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

    # --- TAB 4: SIMULATOR (MODEL ASLI) ---
    with tab4:
        st.markdown("### 🔮 Prediction Simulator (Real Model)")
        st.write("Masukkan profil nasabah untuk memprediksi churn menggunakan Model XGBoost.")
        
        # Load Model
        pipeline = load_model()
        
        # --- INPUT FORM ---
        with st.container(border=True):
            c_in1, c_in2, c_in3 = st.columns(3)
            with c_in1:
                # Input disesuaikan dengan fitur model
                gender = st.selectbox("Gender", ["M", "F"])
                age = st.selectbox("Age Group", ["Young", "Adult", "Senior"]) # Dummy mapping nanti
                marital = st.selectbox("Marital Status", ["Married", "Single", "Divorced", "Unknown"])
                tenure = st.slider("Tenure (Bulan)", 0, 60, 36)
            with c_in2:
                products = st.slider("Total Produk (Relationship)", 1, 6, 2)
                inactive = st.slider("Bulan Tidak Aktif (12 bln)", 0, 12, 1)
                contacts = st.slider("Jumlah Komplain (12 bln)", 0, 6, 2)
                card = st.selectbox("Tipe Kartu", ["Blue", "Silver", "Gold", "Platinum"])
            with c_in3:
                trans_ct = st.number_input("Total Transaksi (1 thn)", 0, 150, 40)
                trans_amt = st.number_input("Nominal Transaksi ($)", 0, 20000, 2000)
                revolving = st.number_input("Saldo Kredit ($)", 0, 3000, 1000)
                util_ratio = st.slider("Utilisasi Limit", 0.0, 1.0, 0.1)

            predict_btn = st.button("🔍 Prediksi Risiko Churn", use_container_width=True)

        # --- LOGIKA PREDIKSI ---
        if predict_btn:
            if pipeline:
                try:
                    # Bikin DataFrame (Format harus SAMA PERSIS dengan saat Training)
                    input_df = pd.DataFrame([{
                        'Customer_Age': 45, # Dummy default
                        'Gender': gender,
                        'Dependent_count': 2, # Dummy default
                        'Education_Level': 'Graduate', # Dummy default
                        'Marital_Status': marital,
                        'Income_Category': '$60K - $80K', # Dummy default
                        'Card_Category': card,
                        'Months_on_book': tenure,
                        'Total_Relationship_Count': products,
                        'Months_Inactive_12_mon': inactive,
                        'Contacts_Count_12_mon': contacts,
                        'Credit_Limit': 10000, # Dummy default
                        'Total_Revolving_Bal': revolving,
                        'Avg_Open_To_Buy': 9000, # Dummy default
                        'Total_Amt_Chng_Q4_Q1': 0.7, # Dummy default
                        'Total_Trans_Amt': trans_amt,
                        'Total_Trans_Ct': trans_ct,
                        'Total_Ct_Chng_Q4_Q1': 0.6, # Dummy default
                        'Avg_Utilization_Ratio': util_ratio
                    }])

                    # Pastikan nama kolom lowercase (jika pipeline mengharapkan lowercase)
                    input_df.columns = [x.lower() for x in input_df.columns]
                    
                    # PREDIKSI MENGGUNAKAN MODEL ASLI
                    prediction = pipeline.predict(input_df)[0]
                    prob = pipeline.predict_proba(input_df)[0][1]

                    # TAMPILKAN HASIL
                    st.divider()
                    c_res1, c_res2 = st.columns([1, 2])
                    
                    with c_res1:
                        if prob > 0.5:
                            st.error("HIGH RISK (CHURN)")
                            st.metric("Probability", f"{prob*100:.2f}%")
                        else:
                            st.success("LOW RISK (AMAN)")
                            st.metric("Probability", f"{prob*100:.2f}%")
                    
                    with c_res2:
                        st.info("💡 **Model Insight:**")
                        st.write(f"Model memprediksi nasabah ini memiliki peluang {prob*100:.1f}% untuk berhenti berlangganan.")
                        if prob > 0.5:
                            st.write("**Rekomendasi:** Segera hubungi nasabah untuk retensi.")
                        else:
                            st.write("**Rekomendasi:** Tawarkan produk cross-selling.")

                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan saat memproses data ke model: {e}")
                    st.warning("Pastikan input data (nama kolom/tipe data) sesuai dengan format training model.")
            else:
                st.error("⚠️ Model belum dimuat. Tidak dapat melakukan prediksi.")
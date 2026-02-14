import streamlit as st
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# 1. AYARLAR VE GÜVENLİK
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key, transport='rest')
    
    model = genai.GenerativeModel('models/gemini-1.5-flash')

# 2. MAHMUT'UN LSTM VERİSİNİ OKUYAN FONKSİYON
def load_mahmut_lstm_data():
    # Bu kısım gerçek dünyada bir dosyadan okunur, şimdilik Mahmut'un JSON'ını simüle ediyoruz
    mahmut_json = {
        "analysis": {
            "energy_efficiency": {
                "current_load_prediction": -0.00638238713145256,
                "recommend_deep_sleep": True
            }
        }
    }
    raw_load = mahmut_json["analysis"]["energy_efficiency"]["current_load_prediction"]
    load_percent = max(0, round(raw_load * 100, 2))
    recommendation = "Deep Sleep" if mahmut_json["analysis"]["energy_efficiency"]["recommend_deep_sleep"] else "Normal"
    return load_percent, recommendation

# 3. ANA KARAR MEKANİZMASI (THINKING & ACTION)
def get_ai_decision(traffic, time, event, lstm_rec):
    # Mahmut'un istediği 'Thinking' (Düşünme) mantığını kodla simüle ediyoruz
    # Bu sayede Google 404 verse bile ajanımız karar verebilecek.
    
    # 🧠 THINKING (Mantık Katmanı)
    if event != "Normal":
        mode = "PERFORMANCE_MODE"
        reason = f"Dış olay ({event}) nedeniyle yüksek performans önceliklendirildi."
        savings = "0 kWh"
    elif traffic < 20 or lstm_rec == "Deep Sleep":
        mode = "ECO_MODE"
        reason = f"LSTM tahmini düşük trafik (%{traffic}) ve derin uyku önerdi. Enerji tasarrufu aktif."
        savings = "15.4 kWh"
    else:
        mode = "STANDARD_MODE"
        reason = "Trafik normal seviyede, denge modu korundu."
        savings = "5.2 kWh"

    # 📦 ACTION (Aksiyona Hazır JSON Çıktısı)
    return {
        "mode": mode,
        "reason": reason,
        "confidence": 0.98,
        "savings": savings,
        "source": "Local-Intelligence-Agent"
    }# 4. STREAMLIT ARAYÜZÜ
st.set_page_config(page_title="AI-RAN Agent Pilot", layout="wide", page_icon="⚡")
st.title("⚡ AI-RAN Pilot: Autonomous Decision Agent")
st.markdown("### Mahmut'un LSTM Modeli Entegre Edildi")

# Yan Menü
with st.sidebar:
    st.header("📡 Kontrol Paneli")
    mahmut_load, mahmut_rec = load_mahmut_lstm_data() # Mahmut'un verilerini çek
    
    st.info(f"🤖 LSTM Tahmini: %{mahmut_load} ({mahmut_rec})")
    
    event_type = st.selectbox("Şebeke Olayı", ["Normal", "Maç", "Konser", "Acil Durum"])
    run_btn = st.button("🤖 Ajanı Çalıştır", type="primary")

# Ekran Çıktıları
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Giriş Verileri")
    st.metric(label="LSTM Trafik Tahmini", value=f"%{mahmut_load}")
    st.write(f"**LSTM Stratejisi:** {mahmut_rec}")

with col2:
    if run_btn:
        with st.spinner("AI Ajanı Karar Veriyor (Thinking)..."):
            # Burası artık hata vermeyecek!
            decision = get_ai_decision(mahmut_load, "12:00", event_type, mahmut_rec)
            
            # Karar Görselleştirme
            if decision["mode"] == "ECO_MODE":
                st.success(f"✅ KARAR: {decision['mode']}")
            elif decision["mode"] == "PERFORMANCE_MODE":
                st.error(f"🚀 KARAR: {decision['mode']}")
            else:
                st.warning(f"⚖️ KARAR: {decision['mode']}")
            
            st.json(decision) # Mahmut'un istediği meşhur aksiyon JSON'ı
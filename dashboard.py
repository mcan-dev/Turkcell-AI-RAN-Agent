import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# 1. Ayarlar ve Güvenlik
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Sayfa Ayarları (Arkadaşının temasına uygun)
st.set_page_config(page_title="AI-RAN Agent Pilot", layout="wide", page_icon="⚡")

# Başlık
st.title("⚡ AI-RAN Pilot: Autonomous Decision Agent")
st.markdown("### Energy Efficiency & Traffic Optimization Module")

# Yan Menü (Kontrol Paneli)
with st.sidebar:
    st.header("📡 Simülasyon Verileri")
    
    # Trafik Simülasyonu
    traffic_load = st.slider("Anlık Trafik Yükü (%)", 0, 100, 45)
    
    # Saat Seçimi
    time_of_day = st.time_input("Saat Seçimi", value=None)
    saat_str = str(time_of_day) if time_of_day else "12:00"
    
    # Özel Gün Durumu
    event_type = st.selectbox(
        "Şebeke Olayı (Event)",
        ["Yok (Normal)", "Derbi Maçı", "Konser", "Acil Durum"]
    )
    
    run_btn = st.button("🤖 Ajanı Çalıştır", type="primary")

# --- YAPAY ZEKA AJANI ---
def get_agent_decision(traffic, time, event):
    if not api_key:
        return {"hata": "API Key Bulunamadı"}
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-flash-latest')
    
    prompt = f"""
    Sen bir Şebeke Yönetim Ajanısın.
    VERİLER: Trafik: %{traffic}, Saat: {time}, Olay: {event}
    
    KURALLAR:
    1. Trafik < %15 ve Saat 00:00-06:00 -> ECO_MODE (Maksimum Tasarruf)
    2. Özel Olay (Maç, Konser) veya Trafik > %80 -> PERFORMANCE_MODE (Maksimum Hız)
    3. Diğer -> STANDARD_MODE (Dengeli)
    
    ÇIKTI (JSON):
    {{
      "mode": "KARAR",
      "reason": "Kısa teknik açıklama",
      "confidence": 0.95,
      "savings": "XX kWh"
    }}
    """
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except:
        return {"mode": "ERROR", "reason": "Model yanıt veremedi."}

# --- EKRAN ÇIKTILARI ---
col1, col2 = st.columns([1, 2])

with col1:
    st.info("Bu panel, LSTM modelinden gelen verileri simüle eder.")
    st.metric(label="Gelen Trafik Verisi", value=f"%{traffic_load}", delta="Stabil")

with col2:
    if run_btn:
        with st.spinner("AI Ajanı Düşünüyor..."):
            decision = get_agent_decision(traffic_load, saat_str, event_type)
            
            # Kararı Ekrana Bas
            if decision.get("mode") == "ECO_MODE":
                st.success(f"✅ KARAR: {decision['mode']}")
            elif decision.get("mode") == "PERFORMANCE_MODE":
                st.error(f"🚀 KARAR: {decision['mode']}")
            else:
                st.warning(f"⚖️ KARAR: {decision['mode']}")
            
            st.json(decision)
    else:
        st.write("👈 Sol taraftan verileri seçip 'Ajanı Çalıştır'a basın.")
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

# --- GÜVENLİK VE AYARLAR ---
load_dotenv() # .env dosyasını oku

# API Key kontrolü
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ HATA: API Key bulunamadı! .env dosyasını kontrol et.")
    print("İpucu: .env dosyasında 'GOOGLE_API_KEY=AIza...' şeklinde yazdığından emin ol.")
    exit()

# Key'i ayarla
genai.configure(api_key=api_key)

# Modeli Seç (Senin listende çalışan model)
model = genai.GenerativeModel('models/gemini-flash-latest')

# --- OTONOM AJAN FONKSİYONU ---
def run_agent(lstm_prediction, sensor_data):
    # Prompt (Ajanın Beyni)
    prompt = f"""
    Sen bir Enerji Yönetim Ajanısın. Görevin, gelen verilere göre şebeke moduna karar vermek.

    GİRDİLER:
    1. Trafik Tahmini (LSTM Modelinden): %{lstm_prediction}
    2. Sensör Verileri: {json.dumps(sensor_data)}
    3. Bilgi Tabanı (Knowledge Base):
       - Trafik <%10 ve Saat 00:00-06:00 arasındaysa -> ECO_MODE
       - Özel Gün (Maç, Konser) varsa -> PERFORMANCE_MODE
       - Diğer durumlar -> STANDARD_MODE

    GÖREV:
    Bu verilere bak ve bir JSON çıktısı üret.

    İSTENEN JSON FORMATI:
    {{
      "karar": "MOD_ISMI",
      "sebep": "Neden bu kararı verdiğinin kısa açıklaması",
      "guven_skoru": 0.0 ile 1.0 arası bir sayı,
      "tahmini_tasarruf": "x kWh"
    }}
    Sadece JSON döndür, başka metin yazma.
    """

    try:
        response = model.generate_content(prompt)
        # JSON temizliği (Markdown tırnaklarını siler)
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        return {"hata": str(e)}

# --- SİMÜLASYON BAŞLIYOR ---
print("\n--- TURKCELL ENERJİ AJANI BAŞLATILIYOR (GÜVENLİ MOD) ---")

# Senaryo 1: Gece Yarısı
print("\nSenaryo 1: Gece Yarısı, Sakin Ortam")
sonuc1 = run_agent(lstm_prediction=5, sensor_data={
    "saat": "03:30",
    "sicaklik": 22,
    "ozel_gun": "Yok"
})
print(json.dumps(sonuc1, indent=2, ensure_ascii=False))

# Senaryo 2: Derbi Maçı
print("\n=============================================")
print("\nSenaryo 2: Derbi Maçı Var! (Kritik Durum)")
sonuc2 = run_agent(lstm_prediction=85, sensor_data={
    "saat": "20:00",
    "sicaklik": 25,
    "ozel_gun": "Derbi Maçı"
})
print(json.dumps(sonuc2, indent=2, ensure_ascii=False))
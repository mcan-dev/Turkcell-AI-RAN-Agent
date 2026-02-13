import google.generativeai as genai

# --- BURAYA KENDİ API KEY'İNİ YAPIŞTIR ---
API_KEY = "AIzaSyAl70BL_WJ5nSJ62QZ2fp-JPXAJk--Vr4o"

genai.configure(api_key=API_KEY)

print("--- LİSTE ALINIYOR... ---")

try:
    # Google'a soruyoruz: Elimde hangi modeller var?
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Kullanabileceğin Model İsmi: {m.name}")
except Exception as e:
    print("HATA OLUŞTU:", e)

print("--------------------------")
import os
from dotenv import load_dotenv
import google.generativeai as genai # Bu satırı eklemeyi unutma

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key) 

print("--- LİSTE ALINIYOR... ---")
try:
    # Google'a soruyoruz: Elimde hangi modeller var?
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Kullanabileceğin Model İsmi: {m.name}")
except Exception as e:
    print("HATA OLUŞTU:", e)

print("--------------------------")
# scripts/check_models.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Projenin ana dizinindeki .env dosyasını bulmak için
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# API anahtarını ortam değişkenlerinden al
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("HATA: GEMINI_API_KEY bulunamadı. Lütfen projenizin ana dizinindeki .env dosyasını kontrol edin.")
else:
    genai.configure(api_key=api_key)
    print("API Anahtarı bulundu. Mevcut ve metin üretebilen modeller listeleniyor...\n")
    
    try:
        for m in genai.list_models():
            # Sadece 'generateContent' metodunu destekleyen modelleri listele
            if 'generateContent' in m.supported_generation_methods:
                print(f"- Model Adı: {m.name}")
        
        print("\nLütfen yukarıdaki listeden bir model adı seçip ('models/' kısmıyla birlikte) bana bildirin.")
        print("Genellikle 'models/gemini-1.5-flash-latest' veya 'models/gemini-pro' iyi bir seçimdir.")

    except Exception as e:
        print(f"Modeller listelenirken bir hata oluştu: {e}")
        print("Lütfen API anahtarınızın doğru olduğundan ve Google Cloud projenizde 'Generative Language API'nin etkinleştirildiğinden emin olun.")

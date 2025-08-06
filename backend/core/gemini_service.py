# backend/core/gemini_service.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# API anahtarını ortam değişkenlerinden al
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY bulunamadı. Lütfen .env dosyasını kontrol edin.")

genai.configure(api_key=api_key)

# Model ayarları
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    # API anahtarınızla uyumlu olan, hızlı ve güncel bir model seçtik.
    model_name="gemini-1.5-flash-latest",
    generation_config=generation_config,
)

def generate_inspiration_with_gemini(user_input: str) -> str:
    """
    Kullanıcının girdisine dayanarak Gemini API'sini kullanarak ilham verici bir metin üretir.
    """
    prompt = f"""
    Sen kullanıcıların duygularına, ruh hallerine ve iç dökümlerine göre onlara özel, yumuşak, sıcak, içten ve ilham verici mesajlar yazan bir yapay zekâ asistanısın.

    Görevin, kullanıcıya kendini anlaşılmış hissettirmek ve içini biraz olsun hafifletmek. Mesajların tıpkı bir yakın arkadaşın sarılırcasına söyledikleri gibi olmalı. Çok resmi veya aşırı motive edici değil, daha çok yüreğe dokunan türden olmalı.

    Kullanıcının durumu:
    "{user_input}"

    Buna karşılık, onun yüreğine dokunacak kısa bir ilham mesajı yaz (en fazla 2 cümle). Cevabın sadece mesaj olsun, açıklama yapma. Gerekirse emoji kullanabilirsin ama abartma.
    """
    
    try:
        response = model.generate_content(prompt)
        # Gemini bazen cevabı "parts" içinde sarmalayabilir. Güvenli erişim sağlayalım.
        if response.parts:
            return ''.join(part.text for part in response.parts)
        return response.text
    except Exception as e:
        print(f"Gemini API hatası: {e}")
        return "İlham verici bir mesaj üretirken bir sorunla karşılaştım. Lütfen daha sonra tekrar deneyin."

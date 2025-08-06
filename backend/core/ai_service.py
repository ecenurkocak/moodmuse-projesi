from ..core.config import settings
import httpx
from langchain_openai import ChatOpenAI
import re
import json
import random
from .spotify_service import get_spotify_access_token, search_spotify_playlist
from ..core.gemini_service import generate_inspiration_with_gemini # Gemini servisimizi import ediyoruz

llm = ChatOpenAI(
    temperature=0.7,
    openai_api_base=f"{settings.AI_SERVICE_URL}/v1",
    openai_api_key="sk-111111111111111111111111111111111111111111111111",
    model_name="local-model"
)

# Duyguları, Colormind API'sinin modelleriyle eşleştiriyoruz.
MOOD_TO_COLORMIND_MODEL = {
    "mutlu": "default",
    "üzgün": "ui",
    "kızgın": "default",
    "şaşkın": "default",
    "sakin": "ui",
    "enerjik": "default",
    "düşünceli": "ui",
    "kararsız": "default",
    "karmaşık": "default"
}

async def generate_palette_from_colormind(mood_label: str) -> list[str]:
    """Colormind API'sini kullanarak duyguya uygun, AI tabanlı bir renk paleti oluşturur."""
    model = MOOD_TO_COLORMIND_MODEL.get(mood_label, "default")
    payload = {"model": model}

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post("http://colormind.io/api/", json=payload)
            response.raise_for_status()
            rgb_palette = response.json().get("result", [])
            hex_palette = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in rgb_palette]
            return hex_palette[:4]
    except Exception as e:
        print(f"Colormind API hatası: {e}")
        return ["#D3D3D3", "#A9A9A9", "#808080", "#696969"]

async def get_ai_suggestions(text: str) -> dict:
    """
    Kullanıcı metninden duygu tahmini yapar, Colormind ile renk paleti üretir,
    ve diğer önerileri dinamik olarak oluşturur.
    """
    try:
        # Adım 1: Duygu Analizi (Yerel model ile)
        mood_prompt = (
            f"Verilen metnin ana duygusunu şu listeden birini seçerek belirle: "
            f"mutlu, üzgün, kızgın, şaşkın, sakin, enerjik, düşünceli, kararsız. "
            f"Cevabı SADECE tek kelime olarak, örneğin 'mutlu' şeklinde ver.\n\n"
            f"Metin: \"{text}\""
        )
        mood_response = await llm.ainvoke(mood_prompt)
        full_response = mood_response.content.strip()
        mood_label = full_response.split()[0].lower().strip('(),."')

        if mood_label not in MOOD_TO_COLORMIND_MODEL:
            mood_label = "karmaşık"

        # Adım 2: Colormind API'sinden Renk Paleti Alımı
        color_list = await generate_palette_from_colormind(mood_label)

        # Adım 3: İlham Sözü Üretimi (Google Gemini ile)
        # Gemini'ye hem kullanıcının orijinal metnini hem de çıkardığımız duygu etiketini göndererek
        # daha zengin bir bağlam sunabiliriz.
        gemini_prompt = f"Kullanıcı '{mood_label}' hissettiğini ve gününün şöyle geçtiğini belirtti: '{text}'. Ona özel, kısa, dramatik olmayan, içten ve sade bir Türkçe motivasyon cümlesi üret."
        inspirational_quote = generate_inspiration_with_gemini(gemini_prompt)

        # Adım 4: Spotify Playlist Bulma
        spotify_token = await get_spotify_access_token()
        playlist_url = "https://open.spotify.com/search/error"
        if spotify_token:
            search_term = f"{mood_label} ruh hali müzik"
            playlist_url = await search_spotify_playlist(search_term, spotify_token)

        return {
            "mood_label": mood_label,
            "color_palette": color_list,
            "spotify_playlist": playlist_url,
            "inspirational_quote": inspirational_quote,
        }

    except Exception as e:
        print(f"Öneri üretimi sırasında hata oluştu: {e}")
        return {"error": "AI servisinden yanıt alınamadı."}

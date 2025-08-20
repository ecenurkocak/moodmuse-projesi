import os
import asyncio
import re
from typing import Dict, Any

from backend.core.config import settings
from backend.core.ai_service import generate_palette_from_colormind
from backend.core.spotify_service import get_spotify_access_token, search_spotify_playlist
from backend.core.gemini_service import generate_inspiration_with_gemini


async def generate_content_for_mood(mood: str, user_text: str) -> Dict[str, Any]:
    """
    Belirtilen duygu durumuna göre kişiselleştirilmiş içerik üretir.
    Ana uygulamadaki (ai_service) modern ve kaliteli mantığı kullanır.
    """
    if not mood:
        raise ValueError("Duygu durumu boş olamaz.")

    try:
        # llm = ChatOpenAI(
        #     temperature=0.7,
        #     openai_api_base=f"{settings.AI_SERVICE_URL}/v1",
        #     openai_api_key="sk-111111111111111111111111111111111111111111111111",
        #     model_name="local-model"
        # )
        
        print(f"'{mood}' için e-posta içeriği üretiliyor...")

        # 1. Profesyonel Renk Paleti (Colormind API)
        color_palette_list = await generate_palette_from_colormind(mood)
        color_palette_str = ", ".join(color_palette_list)
        print(f"Renk paleti üretildi: {color_palette_str}")

        # 2. Kaliteli Alıntı (Yönlendirilmiş Prompt)
        print(f"Gemini için user_text: '{user_text}'")
        quote = generate_inspiration_with_gemini(user_text)
        print(f"Gemini'den gelen ilham sözü (raw): '{quote}'")
        if not quote:
            quote = "Bu hafta sana özel bir söz bulamadık ama gelecek hafta daha iyi olacak!"

        print(f"Son ilham sözü: '{quote}'")
        
        # 3. Akıllı Spotify Listesi
        print("Spotify erişim tokenı alınıyor...")
        spotify_token = await get_spotify_access_token()
        if spotify_token:
            print("Spotify erişim tokenı başarıyla alındı.")
            search_term = f"{mood} ruh hali müzik"
            print(f"Spotify için arama terimi: '{search_term}'")
            playlist_url = await search_spotify_playlist(search_term, spotify_token)
            print(f"Spotify'dan gelen playlist URL'si: '{playlist_url}'")
            if playlist_url:
                spotify_url = playlist_url
            else:
                print("Spotify playlist bulunamadı, varsayılan URL kullanılıyor.")
        else:
            print("Spotify erişim tokenı alınamadı, varsayılan URL kullanılıyor.")
        print(f"Son Spotify URL'si: {spotify_url}")

        return {
            "quote": quote,
            "spotify_url": spotify_url,
            "color_palette": color_palette_str
        }

    except Exception as e:
        print(f"İçerik üretilirken bir hata oluştu: {e}")
        return {
            "quote": "Bu hafta sana özel bir söz bulamadık ama gelecek hafta daha iyi olacak!",
            "spotify_url": "https://open.spotify.com/",
            "color_palette": "#FFFFFF, #000000, #808080"
        }

if __name__ == '__main__':
    mood = "hüzünlü"
    # Asenkron fonksiyonu çalıştırmak için asyncio.run kullanılır
    content = asyncio.run(generate_content_for_mood(mood))
    print("\n--- Üretilen İçerik ---")
    print(f"İlham Sözü: {content['quote']}")
    print(f"Spotify Listesi: {content['spotify_url']}")
    print(f"Renk Paleti: {content['color_palette']}")
    print("-------------------------")

import os
import asyncio
import re
from langchain_openai import ChatOpenAI
from typing import Dict, Any

from core.config import settings
from core.ai_service import generate_palette_from_colormind
from core.spotify_service import get_spotify_access_token, search_spotify_playlist


async def generate_content_for_mood(mood: str, user_text: str) -> Dict[str, Any]:
    """
    Belirtilen duygu durumuna göre kişiselleştirilmiş içerik üretir.
    Ana uygulamadaki (ai_service) modern ve kaliteli mantığı kullanır.
    """
    if not mood:
        raise ValueError("Duygu durumu boş olamaz.")

    try:
        llm = ChatOpenAI(
            temperature=0.7,
            openai_api_base=f"{settings.AI_SERVICE_URL}/v1",
            openai_api_key="sk-111111111111111111111111111111111111111111111111",
            model_name="local-model"
        )
        
        print(f"'{mood}' için e-posta içeriği üretiliyor...")

        # 1. Profesyonel Renk Paleti (Colormind API)
        color_palette_list = await generate_palette_from_colormind(mood)
        color_palette_str = ", ".join(color_palette_list)
        print("Renk paleti üretildi.")

        # 2. Kaliteli Alıntı (Yönlendirilmiş Prompt)
        quote_prompt = f"""'{mood}' duygusuna uygun, kısa, dramatik olmayan, içten ve sade bir Türkçe motivasyon cümlesi üret.
Sadece şu formatta yaz: Söz: "..." """
        quote_response = await llm.ainvoke(quote_prompt)
        content = quote_response.content.strip()
        quote_match = re.search(r"Söz:\s*[\"'](.+?)[\"']", content)
        quote = quote_match.group(1).strip() if quote_match else "Gelecek hafta daha iyi olacak!"
        print("İlham sözü üretildi.")
        
        # 3. Akıllı Spotify Listesi
        spotify_token = await get_spotify_access_token()
        spotify_url = "https://open.spotify.com/"
        if spotify_token:
            search_term = f"{mood} ruh hali müzik"
            playlist_url = await search_spotify_playlist(search_term, spotify_token)
            if playlist_url:
                spotify_url = playlist_url
        print("Spotify listesi bulundu.")

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

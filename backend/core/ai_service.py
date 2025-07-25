import os
import google.generativeai as genai
from .config import settings

# Google API anahtarını ortam değişkeninden al
# Bu satırı, anahtarınızı güvenli bir şekilde yönetmek için kullanın
# os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
genai.configure(api_key=settings.GOOGLE_API_KEY)

import random
from typing import Dict, List


def analyze_sentiment(text: str) -> str:
    """
    Metnin duygu etiketini analiz eder (placeholder).
    Şimdilik rastgele bir duygu döndürüyor.
    """
    sentiments = ["mutlu", "üzgün", "kızgın", "sakin", "enerjik"]
    return random.choice(sentiments)


def generate_color_palette(mood: str) -> List[str]:
    """Duyguya göre bir renk paleti oluşturur (placeholder)."""
    palettes = {
        "mutlu": ["#FFD700", "#FFA500", "#FF6347", "#FFFFFF", "#F0E68C"],
        "üzgün": ["#4682B4", "#708090", "#B0C4DE", "#FFFFFF", "#696969"],
        "kızgın": ["#DC143C", "#FF0000", "#8B0000", "#FFFFFF", "#000000"],
        "sakin": ["#E0FFFF", "#AFEEEE", "#7FFFD4", "#FFFFFF", "#F5F5F5"],
        "enerjik": ["#FF4500", "#FF8C00", "#FFD700", "#FFFFFF", "#32CD32"],
    }
    return palettes.get(mood, ["#FFFFFF", "#000000", "#808080", "#C0C0C0", "#A9A9A9"])


def get_spotify_playlist(mood: str) -> str:
    """Duyguya uygun bir Spotify listesi URL'si döndürür (placeholder)."""
    playlists = {
        "mutlu": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aJc1uA",
        "üzgün": "https://open.spotify.com/playlist/37i9dQZF1DWSqBruwoIXkA",
        "kızgın": "https://open.spotify.com/playlist/37i9dQZF1DX1tyCD9QhIWF",
        "sakin": "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO",
        "enerjik": "https://open.spotify.com/playlist/37i9dQZF1DX8a1c5ay63hT",
    }
    return playlists.get(mood, "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M")


def generate_inspirational_quote(mood: str) -> str:
    """Duyguya uygun ilham verici bir söz üretir (placeholder)."""
    quotes = {
        "mutlu": "Hayat bisiklete binmek gibidir. Dengenizi korumak için hareket etmeye devam etmelisiniz. - Albert Einstein",
        "üzgün": "En karanlık gece bile sona erer ve güneş tekrar doğar. - Victor Hugo",
        "kızgın": "Öfke anında sabır gösteren, yüz günlük hüzünden kurtulur. - Çin Atasözü",
        "sakin": "Huzur, içinde gürültü olmayan bir yer değil, gürültünün ortasında sakin kalabilmektir.",
        "enerjik": "Yapabileceğinize inanın, böylece yolun yarısını gitmiş olursunuz. - Theodore Roosevelt",
    }
    return quotes.get(mood, "Her gün yeni bir başlangıçtır.")


async def get_ai_suggestions(text: str) -> Dict[str, str | List[str]]:
    """
    Ana fonksiyon: Metni analiz eder ve tüm önerileri bir arada döndürür.
    """
    mood = analyze_sentiment(text)
    
    suggestions = {
        "mood_label": mood,
        "color_palette": generate_color_palette(mood),
        "spotify_playlist": get_spotify_playlist(mood),
        "inspirational_quote": generate_inspirational_quote(mood),
    }
    
    return suggestions 
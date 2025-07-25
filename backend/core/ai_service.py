import httpx
import base64
import random
from typing import Dict, List, Any
from .config import settings

# Hugging Face model ve API bilgileri
HF_TRANSLATION_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-tr-en"
HF_EMOTION_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
HF_HEADERS = {"Authorization": f"Bearer {settings.HUGGING_FACE_API_KEY}"}


async def translate_tr_to_en(text: str) -> str:
    # ... (Bu fonksiyon değişmedi)
    payload = {"inputs": text}
    async with httpx.AsyncClient(timeout=30.0) as client:
        print(f"Translating text: '{text}'")
        response = await client.post(HF_TRANSLATION_URL, headers=HF_HEADERS, json=payload)

    if response.status_code != 200:
        print(f"Error during translation: {response.text}")
        return text

    translated_text = response.json()[0]['translation_text']
    print(f"Translated text: '{translated_text}'")
    return translated_text


async def query_emotion_model(text: str) -> List[Dict[str, Any]]:
    # ... (Bu fonksiyon değişmedi)
    payload = {"inputs": text}
    async with httpx.AsyncClient(timeout=30.0) as client:
        print(f"Sending request to Emotion model with text: '{text}'")
        response = await client.post(HF_EMOTION_URL, headers=HF_HEADERS, json=payload)
        print(f"Received response from Emotion model. Status: {response.status_code}")

    if response.status_code != 200:
        if response.status_code == 503 and "is currently loading" in response.text:
            raise Exception("AI model is currently loading, please try again in a moment.")
        raise Exception(f"Error from AI service: {response.status_code} - {response.text}")

    return response.json()[0]


def map_emotion_to_mood(emotion_label: str) -> str:
    # ... (Bu fonksiyon değişmedi)
    mapping = {
        "joy": "mutlu",
        "sadness": "üzgün",
        "anger": "kızgın",
        "fear": "korkmuş",
        "surprise": "şaşırmış",
        "disgust": "tiksinti",
        "neutral": "sakin",
    }
    return mapping.get(emotion_label, "sakin")


def rgb_to_hex(rgb: List[int]) -> str:
    # ... (Bu fonksiyon değişmedi)
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}".upper()


async def generate_dynamic_color_palette(mood: str) -> List[str]:
    # ... (Bu fonksiyon değişmedi)
    api_url = "http://colormind.io/api/"
    payload = {"model": "default"}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            print(f"Requesting color palette from Colormind API for mood: {mood}")
            response = await client.post(api_url, json=payload)
            response.raise_for_status()

            data = response.json()
            rgb_colors = data.get('result', [])
            hex_colors = [rgb_to_hex(color) for color in rgb_colors]

            print(f"Generated colors from Colormind: {hex_colors}")
            return hex_colors

    except httpx.RequestError as e:
        print(f"Error requesting Colormind API: {e}")
        return ["#FFFFFF", "#000000", "#808080", "#C0C0C0", "#A9A9A9"]


async def get_spotify_access_token() -> str:
    # ... (Bu fonksiyon değişmedi, ancak auth_url'yi gerçek Spotify adresiyle değiştirdim)
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(
        f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}".encode("ascii")
    ).decode("ascii")

    auth_data = {"grant_type": "client_credentials"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            auth_url,
            headers={"Authorization": f"Basic {auth_header}"},
            data=auth_data
        )
    response.raise_for_status()
    return response.json()["access_token"]


# --- YENİ FONKSİYON ---
async def get_spotify_playlist_for_mood(mood: str, access_token: str) -> str:
    """
    Verilen ruh haline göre Spotify'da çalma listesi arar ve rastgele bir tanesini döndürür.
    """
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    search_query = f"{mood} ruh hali"
    
    params = {
        "q": search_query,
        "type": "playlist",
        "market": "TR",
        "limit": 20
    }
    
    print(f"Spotify'da arama yapılıyor: '{search_query}'")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(search_url, headers=headers, params=params)
            response.raise_for_status()

        search_results = response.json()
        playlists = search_results.get("playlists", {}).get("items", [])

        if not playlists:
            print(f"'{mood}' ruh hali için çalma listesi bulunamadı. Varsayılan liste döndürülüyor.")
            return "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6" 

        selected_playlist = random.choice(playlists)
        playlist_url = selected_playlist['external_urls']['spotify']
        
        print(f"Bulunan ve seçilen playlist: {playlist_url}")
        return playlist_url

    except httpx.RequestError as e:
        print(f"[ERROR] Spotify arama sırasında bir hata oluştu: {e}")
        return "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6"
# --- YENİ FONKSİYON SONU ---


def generate_inspirational_quote(mood: str) -> str:
    # ... (Bu fonksiyon değişmedi)
    quotes = {
        "mutlu": "Hayat bisiklete binmek gibidir. Dengenizi korumak için hareket etmeye devam etmelisiniz. - Albert Einstein",
        "üzgün": "En karanlık gece bile sona erer ve güneş tekrar doğar. - Victor Hugo",
        "sakin": "Huzur, içinde gürültü olmayan bir yer değil, gürültünün ortasında sakin kalabilmektir.",
        "kızgın": "Öfke anında sabır gösteren, yüz günlük hüzünden kurtulur. - Çin Atasözü",
        "korkmuş": "Cesaret korkusuzluk değil, korkuya rağmen devam etmektir.",
        "şaşırmış": "Evrenin en anlaşılmaz özelliği, anlaşılabilir olmasıdır. - Albert Einstein",
        "tiksinti": "Olumsuz düşünceleri zihninden uzaklaştırmak, sağlıklı bir başlangıçtır.",
    }
    return quotes.get(mood, "Her gün yeni bir başlangıçtır.")


async def get_ai_suggestions(text: str) -> Dict[str, Any]:
    # ... (Bu fonksiyonun hata yakalama bloğundaki linki de güncelledim)
    try:
        english_text = await translate_tr_to_en(text)
        print(f"[DEBUG] Translated Text: {english_text}")

        model_output = await query_emotion_model(english_text)
        print(f"[DEBUG] Emotion Model Output: {model_output}")

        if not model_output or not isinstance(model_output, list):
            raise Exception("Invalid response format from AI emotion model.")

        highest_emotion = max(model_output, key=lambda x: x['score'])
        emotion_label = highest_emotion['label']
        mood = map_emotion_to_mood(emotion_label)

        print(f"[DEBUG] Highest Emotion: {emotion_label}")
        print(f"[DEBUG] Mapped Mood: {mood}")

        color_palette = await generate_dynamic_color_palette(mood)

        try:
            spotify_token = await get_spotify_access_token()
            spotify_link = await get_spotify_playlist_for_mood(mood, spotify_token)
            print(f"[DEBUG] Spotify Playlist Link: {spotify_link}")
        except Exception as e:
            print(f"[ERROR] Spotify integration error: {e}")
            spotify_link = "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6"

        return {
            "mood_label": mood,
            "color_palette": color_palette,
            "spotify_playlist": spotify_link,
            "inspirational_quote": generate_inspirational_quote(mood),
        }

    except Exception as e:
        print(f"[ERROR] An error occurred in get_ai_suggestions: {e}")
        return {
            "mood_label": "sakin",
            "color_palette": ["#E0FFFF", "#AFEEEE", "#7FFFD4", "#FFFFFF", "#F5F5F5"],
            "spotify_playlist": "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6",
            "inspirational_quote": "Bazen en iyi yanıt, sakin bir nefestir.",
            "error": str(e)
        }

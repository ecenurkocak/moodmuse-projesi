import httpx
import base64
import random
from .config import settings

# Daha uzun bekleme süresi için bir timeout sabiti tanımlayalım
SPOTIFY_TIMEOUT = 15.0

async def get_spotify_access_token() -> str | None:
    """Spotify API için bir erişim token'ı alır."""
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(
        f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}".encode("utf-8")
    ).decode("utf-8")
    
    auth_data = {"grant_type": "client_credentials"}
    headers = {"Authorization": f"Basic {auth_header}"}
    
    async with httpx.AsyncClient(timeout=SPOTIFY_TIMEOUT) as client:
        try:
            response = await client.post(auth_url, data=auth_data, headers=headers)
            response.raise_for_status()
            return response.json().get("access_token")
        except httpx.TimeoutException:
            print("Spotify token alırken zaman aşımı hatası oluştu.")
            return None
        except httpx.HTTPStatusError as e:
            print(f"Spotify token alınırken hata: {e}")
            return None

async def search_spotify_playlist(mood: str, token: str) -> str | None:
    """
    Verilen duyguya göre Spotify'da arama yapar, en alakalı çalma listelerini
    puanlar ve en iyiler arasından rastgele birini seçer.
    """
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    limit = 20
    params = {"q": f"{mood}", "type": "playlist", "limit": limit}
    
    async with httpx.AsyncClient(timeout=SPOTIFY_TIMEOUT) as client:
        try:
            response = await client.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            playlists = response.json().get("playlists", {}).get("items", [])
            
            if not playlists:
                return "https://open.spotify.com/"

            scored_playlists = []
            for index, playlist in enumerate(playlists):
                if not playlist:
                    continue

                current_score = 0
                owner = playlist.get("owner")
                if owner and owner.get("display_name") == "Spotify":
                    current_score += 50
                
                if mood.lower() in playlist.get("name", "").lower():
                    current_score += 25
                    
                current_score += (limit - index)
                
                scored_playlists.append({"playlist": playlist, "score": current_score})

            scored_playlists.sort(key=lambda x: x["score"], reverse=True)
            top_candidates = scored_playlists[:5]

            if not top_candidates:
                 return playlists[0].get("external_urls", {}).get("spotify")

            chosen_one = random.choice(top_candidates)["playlist"]
            return chosen_one.get("external_urls", {}).get("spotify")

        except httpx.TimeoutException:
            print(f"Spotify'da çalma listesi aranırken zaman aşımı hatası oluştu.")
            return "https://open.spotify.com/search/error"
        except httpx.HTTPStatusError as e:
            print(f"Spotify'da arama yapılırken hata: {e}")
            return "https://open.spotify.com/search/error"

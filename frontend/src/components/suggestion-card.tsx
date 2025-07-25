"use client";

type SuggestionCardProps = {
  suggestion: {
    color_palette: string[];
    spotify_playlist: string;
    inspirational_quote: string;
  };
};

const SuggestionCard = ({ suggestion }: SuggestionCardProps) => {
  const { color_palette, spotify_playlist, inspirational_quote } = suggestion;

  // Spotify URL'sini embed edilebilir formata çevir
  const getSpotifyEmbedUrl = (url: string) => {
    try {
      const playlistId = new URL(url).pathname.split('/').pop();
      return `https://open.spotify.com/embed/playlist/${playlistId}?utm_source=generator`;
    } catch (error) {
      console.error("Invalid Spotify URL:", url);
      return ""; // Hatalı URL durumunda boş döner
    }
  };

  const spotifyEmbedUrl = getSpotifyEmbedUrl(spotify_playlist);

  return (
    <div className="bg-card-bg p-8 rounded-xl shadow-lg border border-border-color space-y-8">
      
      {/* Renk Paleti */}
      <div>
        <h3 className="text-2xl font-bold text-primary mb-4">Your Mood Palette</h3>
        <div className="flex flex-wrap gap-4">
          {color_palette.map((color) => (
            <div key={color} className="relative group">
              <div
                style={{ backgroundColor: color }}
                className="w-20 h-20 rounded-full shadow-lg transform group-hover:scale-110 transition-transform border-2 border-white"
              />
              <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 px-2 py-1 bg-text-main text-white text-xs rounded-md opacity-0 group-hover:opacity-100 transition-opacity">
                {color}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Spotify Playlist */}
      {spotifyEmbedUrl && (
        <div>
          <h3 className="text-2xl font-bold text-primary mb-4">Your Soundtrack</h3>
          <iframe
            src={spotifyEmbedUrl}
            width="100%"
            height="352"
            allowFullScreen={false}
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            loading="lazy"
            className="rounded-lg shadow-lg border border-border-color"
          ></iframe>
        </div>
      )}

      {/* İlham Verici Söz */}
      <div>
        <h3 className="text-2xl font-bold text-primary mb-4">Quote of the Day</h3>
        <blockquote className="relative p-4 border-l-4 border-primary bg-bg-main rounded-r-lg">
          <p className="text-xl italic text-text-secondary">
            "{inspirational_quote}"
          </p>
        </blockquote>
      </div>
    </div>
  );
};

export default SuggestionCard; 
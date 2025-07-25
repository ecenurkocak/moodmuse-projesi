'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Loader2 } from 'lucide-react';
import SuggestionCard from '@/components/suggestion-card';

interface AnalysisResponse {
  color_palette: string[];
  spotify_url: string;
  quote: string;
}

export default function Home() {
  const { user, loading: authLoading } = useAuth();
  const [textInput, setTextInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [suggestions, setSuggestions] = useState<AnalysisResponse | null>(null);

  const handleAnalysis = async () => {
    if (textInput.length < 20 || textInput.length > 300) {
      setError('Lütfen 20 ile 300 karakter arasında bir metin girin.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuggestions(null);

    try {
      const response = await fetch('/api/v1/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({ text_input: textInput }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || 'Bir şeyler ters gitti. Lütfen tekrar deneyin.'
        );
      }

      const data: AnalysisResponse = await response.json();
      setSuggestions(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  if (authLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Loader2 className="h-12 w-12 animate-spin text-primary" />
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-20">
        <h1 className="text-5xl font-bold text-primary mb-6">
          Welcome to MoodMuse
        </h1>
        <p className="text-xl text-text-secondary mb-10 max-w-2xl">
          Discover color palettes, music, and inspirational content tailored to your mood.
          Log in to get your personalized analysis.
        </p>
        <div className="flex gap-6">
          <Link href="/login" className="px-8 py-3 text-lg font-semibold rounded-md text-white bg-primary hover:bg-primary-hover transition">
            Login
          </Link>
          <Link href="/register" className="px-8 py-3 text-lg font-semibold rounded-md text-text-main bg-accent-pink hover:opacity-90 transition">
            Register
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto max-w-4xl py-12 px-4">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-primary">
          Merhaba, {user.username}!
        </h1>
        <p className="text-lg text-text-secondary mt-2">
          Bugün nasıl hissediyorsun? Ruh halini bizimle paylaş, sana özel ilham verelim.
        </p>
      </div>

      <div className="bg-background-secondary p-8 rounded-xl shadow-lg">
        <Textarea
          placeholder="Bugün nasıl hissediyorsun? Birkaç kelimeyle anlat..."
          value={textInput}
          onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => {
            setTextInput(e.target.value);
            if (error) setError(null);
          }}
          className="w-full p-4 rounded-md text-base border-2 border-border-color focus:border-primary transition"
          rows={6}
        />
        <div className="flex justify-between items-center mt-4">
          <p className="text-sm text-text-tertiary">
            {textInput.length} / 300
          </p>
          <Button
            onClick={handleAnalysis}
            disabled={
              isLoading || textInput.length < 20 || textInput.length > 300
            }
            className="px-8 py-3 text-lg font-semibold rounded-md text-white bg-primary hover:bg-primary-hover disabled:bg-gray-400 disabled:cursor-not-allowed transition"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Analiz Ediliyor...
              </>
            ) : (
              'İlham Bul'
            )}
          </Button>
        </div>
      </div>

      {error && (
        <div className="mt-6 p-4 bg-red-100 text-red-700 rounded-md text-center">
          {error}
        </div>
      )}

      {suggestions && (
        <div className="mt-12">
          <h2 className="text-3xl font-bold text-center text-primary mb-8">
            İşte Senin İçin Hazırladıklarımız!
          </h2>
          <SuggestionCard
            suggestion={{
              color_palette: suggestions.color_palette,
              spotify_playlist: suggestions.spotify_url,
              inspirational_quote: suggestions.quote,
            }}
          />
        </div>
      )}
    </div>
  );
}

"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '@/services/api';
import SuggestionCard from '@/components/suggestion-card';
import RagQueryCard from '@/components/RagQueryCard';
import { Button } from '@/components/ui/button';

// Backend'den gelen yanıta göre tipleri güncelleyelim
// Bu tipler backend/schemas.py ile uyumlu olmalı
type Suggestion = {
  id: number;
  suggestion_type: string;
  content: string;
};

type AnalysisResponse = {
  color_palette: string[];
  spotify_playlist: string;
  inspirational_quote: string;
};

type MoodEntryResponse = {
  id: number;
  text_input: string;
  mood_label: string;
  created_at: string;
  suggestions: Suggestion[];
};

// SuggestionCard'ın beklediği props formatına dönüştürmek için
type FormattedSuggestion = {
  color_palette: string[];
  spotify_playlist: string;
  inspirational_quote: string;
};

const DashboardPage = () => {
  const router = useRouter();
  const [textInput, setTextInput] = useState('');
  const [analysisResult, setAnalysisResult] = useState<FormattedSuggestion | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Sayfa yüklendiğinde token kontrolü yap
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
    }
  }, [router]);

  const handleAnalysis = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const response = await apiClient.post<AnalysisResponse>('/api/v1/auth/analyze', { text_input: textInput });
      
      const results = response.data;
      
      // Gelen veriyi SuggestionCard'ın beklediği formata dönüştür
      const formatted: FormattedSuggestion = {
        color_palette: results.color_palette,
        spotify_playlist: results.spotify_playlist,
        inspirational_quote: results.inspirational_quote,
      };

      setAnalysisResult(formatted);

    } catch (err: any) {
       if (err.response && err.response.status === 401) {
        // Token geçersizse login'e yönlendir
        setError('Your session has expired. Please log in again.');
        localStorage.removeItem('token');
        router.push('/login');
      } else if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('An error occurred during the analysis. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <form onSubmit={handleAnalysis} className="bg-white/10 backdrop-blur-md p-8 rounded-xl shadow-lg border border-white/20">
        <h1 className="text-4xl font-bold text-center mb-6 text-text-main">
          How are you feeling today?
        </h1>
        <div className="mb-4">
          <label htmlFor="textInput" className="block text-lg font-medium text-text-secondary mb-2">
            Describe your feelings, thoughts, or your day.
          </label>
          <textarea
            id="textInput"
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            className="w-full h-40 p-4 text-black bg-white/10 border border-white/30 rounded-md shadow-sm focus:ring-purple-400 focus:border-purple-400 placeholder:text-gray-500 transition"
            placeholder="e.g., I had a really productive day and I feel energized..."
            required
          />
        </div>
        <Button
          type="submit"
          disabled={isLoading || !textInput}
          className="w-full px-6 py-3 text-lg font-semibold"
        >
          {isLoading ? 'Analyzing...' : 'Analyze My Mood'}
        </Button>
      </form>

      {error && (
        <div className="mt-8 p-4 text-center text-red-400 bg-red-900 border border-red-500 rounded-lg">
          <p>{error}</p>
        </div>
      )}

      {analysisResult && (
        <div className="mt-10 animate-fade-in">
          <h2 className="text-3xl font-bold text-center mb-6">Here are your personalized suggestions:</h2>
          <SuggestionCard suggestion={analysisResult} />
        </div>
      )}

      {/* RAG Sorgu Kartını Buraya Ekle */}
      <RagQueryCard />
      
    </div>
  );
};

export default DashboardPage;

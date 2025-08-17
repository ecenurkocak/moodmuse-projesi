"use client";

import { useState, useEffect, useRef } from 'react'; // useRef eklendi
import { useRouter } from 'next/navigation';
import { addReasoningToEntry } from '@/services/api'; // Yeni import
import apiClient from '@/services/api';
import SuggestionCard from '@/components/suggestion-card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea'; // Textarea import
import { Label } from '@/components/ui/label'; // Label import'unu geri al
import EmojiPicker, { EmojiClickData } from 'emoji-picker-react'; // Emoji Picker import
import { SmilePlus } from 'lucide-react'; // İkon import

// Backend'den gelen yanıta göre tipleri güncelleyelim
// Bu tipler backend/schemas.py ile uyumlu olmalı
type Suggestion = {
  id: number;
  suggestion_type: string;
  content: string;
};

type AnalysisResponse = {
  mood_entry_id: number; // ID eklendi
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
  
  // Emoji için yeni state'ler
  const [selectedEmoji, setSelectedEmoji] = useState<string | null>(null);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const emojiPickerRef = useRef<HTMLDivElement>(null);

  // Reasoning için yeni state'ler
  const [moodEntryId, setMoodEntryId] = useState<number | null>(null);
  const [reasoningText, setReasoningText] = useState('');
  const [isSavingReasoning, setIsSavingReasoning] = useState(false);
  const [reasoningError, setReasoningError] = useState<string | null>(null);
  const [reasoningSaved, setReasoningSaved] = useState(false);


  // Emoji picker dışına tıklamayı dinle
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (emojiPickerRef.current && !emojiPickerRef.current.contains(event.target as Node)) {
        setShowEmojiPicker(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

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
    setMoodEntryId(null); // Resetle
    setReasoningText(''); // Resetle
    setReasoningSaved(false); // Resetle
    // Emoji state'ini resetleme, kullanıcı yeni bir analiz yapana kadar seçili kalabilir.

    try {
      // API isteğine emoji'yi ekle
      const payload = {
        text_input: textInput,
        emoji: selectedEmoji,
      };
      const response = await apiClient.post<AnalysisResponse>('/api/v1/auth/analyze', payload);
      
      const results = response.data;
      setMoodEntryId(results.mood_entry_id); // Gelen ID'yi state'e kaydet
      
      // Gelen veriyi SuggestionCard'ın beklediği formata dönüştür
      const formatted: FormattedSuggestion = {
        color_palette: results.color_palette,
        spotify_playlist: results.spotify_playlist,
        inspirational_quote: results.inspirational_quote,
      };

      setAnalysisResult(formatted);
      setTextInput(''); // Analiz sonrası text input'u temizle
      setSelectedEmoji(null); // Analiz sonrası emoji'yi temizle

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

  const onEmojiClick = (emojiData: EmojiClickData) => {
    setSelectedEmoji(emojiData.emoji);
    setShowEmojiPicker(false);
  };

  // Yeni fonksiyon: 'Neden' metnini kaydeder
  const handleSaveReasoning = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!moodEntryId || !reasoningText) return;

    setIsSavingReasoning(true);
    setReasoningError(null);
    setReasoningSaved(false);

    try {
      await addReasoningToEntry(moodEntryId, reasoningText);
      setReasoningSaved(true);
      // İsteğe bağlı: Bir süre sonra 'Kaydedildi' mesajını kaldır
      setTimeout(() => setReasoningSaved(false), 3000);
    } catch (err) {
      setReasoningError('An error occurred while saving. Please try again.');
    } finally {
      setIsSavingReasoning(false);
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

        {/* Emoji Seçme Alanı */}
        <div className="relative mb-4 flex items-center justify-between">
          <Button type="button" onClick={() => setShowEmojiPicker(!showEmojiPicker)} variant="outline" className="flex items-center gap-2">
            <SmilePlus size={20} />
            {selectedEmoji ? 'Change Emoji' : 'Add an Emoji'}
          </Button>
          {selectedEmoji && <span className="text-4xl">{selectedEmoji}</span>}
          
          {showEmojiPicker && (
            <div ref={emojiPickerRef} className="absolute bottom-full left-0 z-10 mb-2">
              <EmojiPicker onEmojiClick={onEmojiClick} />
            </div>
          )}
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

          {/* Yeni Reasoning Formu */}
          <form onSubmit={handleSaveReasoning} className="mt-8 bg-white/10 backdrop-blur-md p-6 rounded-xl shadow-lg border border-white/20">
            <Label htmlFor="reasoningInput" className="block text-lg font-medium text-text-secondary mb-3">
              Why do you think you feel this way? (Optional)
            </Label>
            <Textarea
              id="reasoningInput"
              value={reasoningText}
              onChange={(e) => setReasoningText(e.target.value)}
              className="w-full h-28 p-4 text-black bg-white/10 border border-white/30 rounded-md shadow-sm focus:ring-purple-400 focus:border-purple-400 placeholder:text-gray-500 transition"
              placeholder="e.g., Because I had a tough meeting at work."
            />
            <div className="mt-4 flex items-center justify-end">
              {reasoningSaved && <p className="text-green-400 mr-4">Saved!</p>}
              <Button
                type="submit"
                disabled={isSavingReasoning || !reasoningText}
                className="px-5 py-2 text-base font-semibold"
              >
                {isSavingReasoning ? 'Saving...' : 'Save'}
              </Button>
            </div>
            {reasoningError && (
              <p className="mt-2 text-sm text-red-400 text-center">{reasoningError}</p>
            )}
          </form>
        </div>
      )}

      
    </div>
  );
};

export default DashboardPage;

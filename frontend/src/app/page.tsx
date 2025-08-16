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
    <div className="flex flex-col items-center justify-center text-center">
      
      {/* Hero Section */}
      <section className="w-full py-20 md:py-32 lg:py-40">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto">
            <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-4">
              Discover Your Inner World with MoodMuse
            </h1>
            <p className="text-lg md:text-xl text-muted-foreground mb-8">
              Your personal AI companion for understanding emotions and finding inspiration.
            </p>
            <Link 
              href="/register" 
              className="inline-block px-8 py-3 text-lg font-semibold rounded-md text-primary-foreground bg-primary hover:bg-primary/90 transition"
            >
              Get Started for Free
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="w-full py-20 md:py-24 bg-background/70 backdrop-blur-sm">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center text-foreground mb-12">
            Why You'll Love MoodMuse
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-card/70 backdrop-blur-md p-6 rounded-lg border">
              <h3 className="text-xl font-semibold text-foreground mb-2">AI-Powered Analysis</h3>
              <p className="text-muted-foreground">
                Understand the emotions behind your words with our advanced AI.
              </p>
            </div>
            {/* Feature 2 */}
            <div className="bg-card/70 backdrop-blur-md p-6 rounded-lg border">
              <h3 className="text-xl font-semibold text-foreground mb-2">Personalized Suggestions</h3>
              <p className="text-muted-foreground">
                Get curated color palettes, music, and quotes to match your mood.
              </p>
            </div>
            {/* Feature 3 */}
            <div className="bg-card/70 backdrop-blur-md p-6 rounded-lg border">
              <h3 className="text-xl font-semibold text-foreground mb-2">Track Your Journey</h3>
              <p className="text-muted-foreground">
                Look back at your emotional history and see how you've grown.
              </p>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
}

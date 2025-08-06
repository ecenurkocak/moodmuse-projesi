"use client";

import { useState } from 'react';
import { queryRag } from '@/services/api';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';

const RagQueryCard = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleQuery = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!question.trim()) return;

    setIsLoading(true);
    setError(null);
    setAnswer('');

    try {
      const response = await queryRag(question);
      setAnswer(response.answer);
    } catch (err) {
      setError('Failed to get an answer. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mt-12 bg-card-bg p-8 rounded-xl shadow-lg border border-border-color">
      <h2 className="text-3xl font-bold text-center mb-6 text-text-main">
        Ask the Mindfulness Expert
      </h2>
      <form onSubmit={handleQuery}>
        <div className="mb-4">
          <label htmlFor="ragQuestion" className="block text-lg font-medium text-text-secondary mb-2">
            What would you like to know about mindfulness or well-being?
          </label>
          <Textarea
            id="ragQuestion"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="w-full h-28 p-4 text-text-main bg-bg-main border border-border-color rounded-md shadow-sm focus:ring-primary focus:border-primary transition"
            placeholder="e.g., How can I practice mindfulness during a busy day?"
            required
          />
        </div>
        <Button
          type="submit"
          disabled={isLoading || !question}
          className="w-full px-6 py-3 text-lg font-semibold"
        >
          {isLoading ? 'Thinking...' : 'Ask'}
        </Button>
      </form>

      {error && (
        <div className="mt-6 p-4 text-center text-red-400 bg-red-900/50 border border-red-500 rounded-lg">
          <p>{error}</p>
        </div>
      )}

      {answer && (
        <div className="mt-8 p-6 bg-bg-main border border-border-color rounded-lg animate-fade-in">
          <h3 className="text-xl font-semibold mb-3 text-text-main">Answer:</h3>
          <p className="text-text-secondary whitespace-pre-wrap">{answer}</p>
        </div>
      )}
    </div>
  );
};

export default RagQueryCard;

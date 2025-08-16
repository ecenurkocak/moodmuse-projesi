"use client";

import { useState } from 'react';
import { queryRag } from '@/services/api';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import ReactMarkdown from 'react-markdown';

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
    <div className="mt-10 bg-card/70 backdrop-blur-md p-8 rounded-xl shadow-lg border">
      <h2 className="text-3xl font-bold text-center mb-6 text-foreground">
        Ask Our AI Assistant
      </h2>
      <form onSubmit={handleQuery} className="space-y-4">
        <div>
          <label htmlFor="rag-query" className="block text-lg font-medium text-muted-foreground mb-2">
            Do you have any questions about mental health topics?
          </label>
          <input
            id="rag-query"
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="w-full p-4 text-foreground bg-background/50 border rounded-md shadow-sm focus:ring-primary focus:border-primary placeholder:text-muted-foreground"
            placeholder="e.g., How can I practice mindfulness?"
          />
        </div>
        <Button 
          type="submit" 
          disabled={isLoading} 
          className="w-full px-6 py-3 text-lg font-semibold text-primary-foreground"
        >
          {isLoading ? 'Thinking...' : 'Ask'}
        </Button>
      </form>

      {error && (
        <div className="mt-6 p-4 text-center text-destructive-foreground bg-destructive/80 border border-destructive rounded-lg">
          <p>{error}</p>
        </div>
      )}

      {answer && (
        <div className="mt-6 p-6 bg-background/50 border rounded-lg">
          <ReactMarkdown className="prose prose-invert max-w-none">
            {answer}
          </ReactMarkdown>
        </div>
      )}
    </div>
  );
};

export default RagQueryCard;



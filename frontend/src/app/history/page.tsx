"use client";

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { getHistory, deleteHistoryEntry } from '@/services/api';
import { MoodEntry } from '@/lib/types';
import { Trash2, Palette, Quote, ListMusic, ChevronLeft, ChevronRight, Loader2, ServerCrash, Inbox } from 'lucide-react';

// Yardımcı Bileşenler

// Renk paletini gösteren bileşen
const ColorPalette = ({ colors }: { colors: string[] }) => (
  <div className="flex space-x-1">
    {colors.map((color, index) => (
      // eslint-disable-next-line
      <div key={index} className="w-6 h-6 rounded-full border border-gray-300" style={{ backgroundColor: color }} />
    ))}
  </div>
);

// Yükleme sırasında gösterilecek iskelet kart
const SkeletonCard = () => (
  <div className="bg-card-bg p-6 rounded-2xl shadow-lg border border-border-color animate-pulse">
    <div className="h-4 bg-gray-300 rounded w-1/4 mb-4"></div>
    <div className="h-6 bg-gray-400 rounded w-full mb-4"></div>
    <div className="flex justify-between items-center">
      <div className="h-8 bg-gray-300 rounded w-1/3"></div>
      <div className="h-8 bg-gray-300 rounded w-1/4"></div>
    </div>
  </div>
);

// Ana Sayfa Bileşeni
const HistoryPage = () => {
  const router = useRouter();
  const [entries, setEntries] = useState<MoodEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [entryToDelete, setEntryToDelete] = useState<number | null>(null);

  const fetchHistory = useCallback(async (page: number) => {
    try {
      setIsLoading(true);
      const data = await getHistory(page, 9);
      setEntries(data.data);
      setTotalPages(Math.ceil(data.total_entries / data.limit));
    } catch (err: any) {
      if (err.response && err.response.status === 401) {
        router.push('/login');
      } else {
        setError('Anılarınızı yüklerken bir sorun oluştu. Lütfen daha sonra tekrar deneyin.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [router]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }
    fetchHistory(currentPage);
  }, [currentPage, fetchHistory, router]);

  const handleDeleteClick = (id: number) => {
    setEntryToDelete(id);
  };

  const confirmDelete = async () => {
    if (entryToDelete === null) return;

    try {
      await deleteHistoryEntry(entryToDelete);
      setEntries(entries.filter(entry => entry.id !== entryToDelete));
      setEntryToDelete(null);
      // Eğer sayfadaki son kartı sildiysek ve ilk sayfa değilse, bir önceki sayfaya git
      if (entries.length === 1 && currentPage > 1) {
        setCurrentPage(currentPage - 1);
      } else {
        // Silme sonrası mevcut sayfayı yeniden yükle
        fetchHistory(currentPage);
      }
    } catch (err) {
      setError('Anıyı silerken bir hata oluştu.');
    }
  };

  const handlePageChange = (newPage: number) => {
    if (newPage < 1 || newPage > totalPages) return;
    setCurrentPage(newPage);
  };
  
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('tr-TR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 9 }).map((_, i) => <SkeletonCard key={i} />)}
        </div>
      );
    }

    if (error) {
      return (
        <div className="text-center py-20 bg-card-bg rounded-lg">
            <ServerCrash className="mx-auto h-16 w-16 text-red-500" />
            <h2 className="mt-4 text-2xl font-semibold text-text-main">Bir Sorun Oluştu</h2>
            <p className="mt-2 text-text-secondary">{error}</p>
        </div>
      );
    }

    if (entries.length === 0) {
      return (
        <div className="text-center py-20 bg-card-bg rounded-lg">
            <Inbox className="mx-auto h-16 w-16 text-gray-400" />
            <h2 className="mt-4 text-2xl font-semibold text-text-main">Henüz Anı Yok</h2>
            <p className="mt-2 text-text-secondary">Analiz yapmaya başladığınızda anılarınız burada görünecek.</p>
        </div>
      );
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {entries.map((entry) => {
          const quote = entry.suggestions.find(s => s.suggestion_type === 'quote')?.content;
          const colorContent = entry.suggestions.find(s => s.suggestion_type === 'color')?.content;
          const colors = colorContent ? colorContent.split(',').map(color => color.trim()) : [];
          const musicLink = entry.suggestions.find(s => s.suggestion_type === 'music')?.content;
          
          return (
            <div key={entry.id} className="bg-white/10 backdrop-blur-md rounded-2xl shadow-lg border border-white/20 flex flex-col justify-between p-6 transition-transform hover:scale-105">
              <div>
                <div className="flex justify-between items-start mb-4">
                  <p className="text-sm text-text-secondary">{formatDate(entry.created_at)}</p>
                  <button onClick={() => handleDeleteClick(entry.id)} className="text-gray-400 hover:text-red-500 transition-colors" title="Anıyı Sil">
                    <Trash2 size={20} />
                  </button>
                </div>
                <p className="text-text-main mb-4 italic">"{entry.text_input}"</p>
              </div>
              <div className="space-y-3">
                {quote && (
                  <div className="flex items-center space-x-2 text-text-secondary">
                    <Quote size={18} />
                    <span className="text-sm flex-1">{quote}</span>
                  </div>
                )}
                {colors.length > 0 && (
                  <div className="flex items-center space-x-2">
                    <Palette size={18} className="text-text-secondary" />
                    <ColorPalette colors={colors} />
                  </div>
                )}
                {musicLink && (
                  <div className="flex items-center space-x-2">
                    <ListMusic size={18} className="text-text-secondary" />
                    <a
                      href={musicLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-green-400 hover:underline flex-1 truncate"
                    >
                      Spotify'da Dinle
                    </a>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 className="text-4xl font-bold text-center my-10 text-text-main">Duygu Arşivin</h1>
      
      {renderContent()}
      
      {totalPages > 1 && (
        <div className="flex justify-center items-center space-x-4 mt-10">
          <button
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1 || isLoading}
            className="p-2 rounded-full bg-card-bg border border-border-color disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-700 transition-colors"
            title="Önceki Sayfa"
          >
            <ChevronLeft size={24} />
          </button>
          <span className="text-text-main font-semibold">
            Sayfa {currentPage} / {totalPages}
          </span>
          <button
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage === totalPages || isLoading}
            className="p-2 rounded-full bg-card-bg border border-border-color disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-700 transition-colors"
            title="Sonraki Sayfa"
          >
            <ChevronRight size={24} />
          </button>
        </div>
      )}

      {entryToDelete !== null && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">
          <div className="bg-white/10 backdrop-blur-md p-8 rounded-lg shadow-2xl max-w-sm w-full border border-white/20">
            <h2 className="text-xl font-bold text-text-main mb-4">Anıyı Sil</h2>
            <p className="text-text-secondary mb-6">Bu anıyı kalıcı olarak silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.</p>
            <div className="flex justify-end space-x-4">
              <button
                onClick={() => setEntryToDelete(null)}
                className="px-4 py-2 rounded-md bg-gray-600 hover:bg-gray-700 transition-colors"
              >
                İptal
              </button>
              <button
                onClick={confirmDelete}
                className="px-4 py-2 rounded-md bg-red-600 hover:bg-red-700 text-white transition-colors flex items-center"
              >
                <Trash2 size={16} className="mr-2"/>
                Sil
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HistoryPage; 
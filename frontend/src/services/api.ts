import axios from 'axios';
import { HistoryResponse } from '@/lib/types';

// Genel Axios Instance (Interceptor'sız)
export const noAuthApiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Kimlik Doğrulamalı Axios Instance (Interceptor'lı)
const authApiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Axios interceptor ile her isteğe token ekleyelim
authApiClient.interceptors.request.use(
  (config) => {
    // Sunucu tarafında (SSR) localStorage'a erişemeyeceğimiz için kontrol ekleyelim
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const getHistory = async (
  page: number = 1,
  limit: number = 9
): Promise<HistoryResponse> => {
  try {
    const response = await authApiClient.get('/api/v1/auth/history', {
      params: { page, limit },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching history:', error);
    throw error;
  }
};

export const deleteHistoryEntry = async (entryId: number): Promise<void> => {
  try {
    await authApiClient.delete(`/api/v1/auth/history/${entryId}`);
  } catch (error)
  {
    console.error(`Error deleting entry ${entryId}:`, error);
    throw error;
  }
};

// RAG sorgusu için yeni fonksiyon
export const queryRag = async (question: string): Promise<{ answer: string }> => {
  try {
    const response = await authApiClient.post('/api/v1/rag/query', { question });
    return response.data;
  } catch (error) {
    console.error('Error querying RAG:', error);
    throw error;
  }
};


export default authApiClient;

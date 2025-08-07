"use client";

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { noAuthApiClient } from '@/services/api';

const RegisterPage = () => {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null); // Başarı durumu için state
  const [isLoading, setIsLoading] = useState(false);

  const handleRegister = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setSuccess(null); // Başlangıçta başarı mesajını temizle
    setIsLoading(true);

    try {
      console.log("Sending registration request...");
      await noAuthApiClient.post('/api/v1/auth/register', {
        username,
        email,
        password,
      });
      
      console.log("Registration successful. Setting success message and redirecting...");
      setSuccess("Registration successful! Redirecting to login...");

      // Yönlendirmeden önce kullanıcıya mesajı görmesi için kısa bir süre verelim.
      setTimeout(() => {
        router.push('/login');
      }, 2000); // 2 saniye sonra yönlendir

    } catch (err: any) {
      console.error("Registration failed:", err);
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      // Başarılı durumda butonu tekrar aktif etmemek için
      if (!success) {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="flex items-center justify-center py-12">
      <div className="w-full max-w-md p-8 space-y-8 bg-white/10 backdrop-blur-md rounded-xl shadow-lg border border-white/20">

        <h2 className="text-3xl font-bold text-center text-text-main">
          Create your Account
        </h2>
        {error && (
          <div className="p-3 my-2 text-sm text-red-400 bg-red-900 border border-red-500 rounded-lg text-center">
            {error}
          </div>
        )}
        {success && (
          <div className="p-3 my-2 text-sm text-green-400 bg-green-900 border border-green-500 rounded-lg text-center">
            {success}
          </div>
        )}
        <form className="space-y-6" onSubmit={handleRegister}>
          <div>
            <label
              htmlFor="username"
              className="text-sm font-medium text-text-secondary"
            >
              Username
            </label>
            <input
              id="username"
              name="username"
              type="text"
              autoComplete="username"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 mt-1 text-black bg-white/10 border border-white/30 rounded-md shadow-sm focus:ring-purple-400 focus:border-purple-400 placeholder:text-gray-300"
            />
          </div>
          <div>
            <label
              htmlFor="email"
              className="text-sm font-medium text-text-secondary"
            >
              Email address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 mt-1 text-black bg-white/10 border border-white/30 rounded-md shadow-sm focus:ring-purple-400 focus:border-purple-400 placeholder:text-gray-300"
            />
          </div>
          <div>
            <label
              htmlFor="password"
              className="text-sm font-medium text-text-secondary"
            >
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="new-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 mt-1 text-black bg-white/10 border border-white/30 rounded-md shadow-sm focus:ring-purple-400 focus:border-purple-400 placeholder:text-gray-300"
            />
          </div>
          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="w-full px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:bg-slate-400"
            >
              {isLoading ? 'Creating Account...' : 'Create Account'}
            </button>
          </div>
        </form>
        <p className="text-sm text-center text-text-secondary">
          Already have an account?{' '}
          <Link
            href="/login"
            className="font-medium text-primary hover:text-primary-hover"
          >
            Login here
          </Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage; 
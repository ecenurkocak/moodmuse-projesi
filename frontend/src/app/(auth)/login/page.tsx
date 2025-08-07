"use client";

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { noAuthApiClient } from '@/services/api';
import { useAuth } from '@/context/AuthContext'; // useAuth hook'unu import et

const LoginPage = () => {
  const router = useRouter();
  const { login } = useAuth(); // Context'ten login fonksiyonunu al
  const [email, setEmail] = useState(''); // Backend username bekliyor, bu yüzden bunu username olarak göndereceğiz
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    const params = new URLSearchParams();
    params.append('username', email); // FastAPI OAuth2PasswordRequestForm 'username' alanı bekliyor
    params.append('password', password);

    try {
      const response = await noAuthApiClient.post('/api/v1/auth/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      
      const { access_token } = response.data;
      if (access_token) {
        login(access_token); // Giriş başarılı olduğunda context'i token ile güncelle
        router.push('/dashboard');
      } else {
        setError('Login failed: No token received.');
      }

    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center py-12">
      <div className="w-full max-w-md p-8 space-y-8 bg-white/10 backdrop-blur-md rounded-xl shadow-lg border border-white/20">
        <h2 className="text-3xl font-bold text-center text-text-main">
          Login to MoodMuse
        </h2>
        {error && (
          <div className="p-3 my-2 text-sm text-red-700 bg-red-100 border border-red-300 rounded-lg text-center">
            {error}
          </div>
        )}
        <form className="space-y-6" onSubmit={handleLogin}>
          <div>
            <label
              htmlFor="email"
              className="text-sm font-medium text-text-secondary"
            >
              Username or Email
            </label>
            <input
              id="email"
              name="email"
              type="text" // Hem username hem email ile giriş yapılabilmesi için text
              autoComplete="username"
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
              autoComplete="current-password"
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
              {isLoading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>
        </form>
        <p className="text-sm text-center text-text-secondary">
          Don't have an account?{' '}
          <Link
            href="/register"
            className="font-medium text-primary hover:text-primary-hover"
          >
            Register here
          </Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage; 
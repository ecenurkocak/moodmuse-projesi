"use client";

import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';

const Navbar = () => {
  const { isAuthenticated, logout } = useAuth();

  return (
    <nav className="bg-primary text-white shadow-md">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Link href="/" className="text-2xl font-bold text-white">
              MoodMuse
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              // Kullanıcı giriş yapmışsa gösterilecekler
              <>
                <Link href="/dashboard" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-hover">
                  Dashboard
                </Link>
                <Link href="/history" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-hover">
                  History
                </Link>
                <button
                  onClick={logout}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white bg-accent-violet hover:opacity-90"
                >
                  Logout
                </button>
              </>
            ) : (
              // Kullanıcı giriş yapmamışsa gösterilecekler
              <>
                <Link href="/login" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-hover">
                  Login
                </Link>
                <Link href="/register" className="px-3 py-2 rounded-md text-sm font-medium text-text-main bg-accent-pink hover:opacity-90">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 
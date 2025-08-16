"use client";

import Link from 'next/link';
import Image from 'next/image';
import { useAuth } from '@/context/AuthContext';

const Navbar = () => {
  const { isAuthenticated, logout } = useAuth();

  return (
    <nav className="bg-[#dec0f1]/30 text-gray-800 shadow-lg py-0">
      <div className="container mx-auto flex items-center justify-between px-6 h-24 sm:h-32 md:h-40">
        
        {/* Logo */}
        <div className="flex items-center h-full">
          <Link href="/" className="flex items-center h-full">
            <Image
              src="/logo.png"
              alt="MoodMuse Logo"
              width={1000}
              height={1000}
              className="h-64 w-auto"
            />
          </Link>
        </div>

        {/* Navigation Links */}
        <div className="flex items-center space-x-4">
          {isAuthenticated ? (
            <>
             <Link
  href="/dashboard"
  className="rounded-lg bg-purple-500/20 px-5 py-2.5 text-lg font-semibold text-white transition-colors duration-200 hover:bg-purple-600"
>
  Dashboard
</Link>

<Link
  href="/history"
  className="rounded-lg bg-purple-500/20 px-5 py-2.5 text-lg font-semibold text-white transition-colors duration-200 hover:bg-purple-600"
>
  History
</Link>

<Link
    href="/profile"
    className="rounded-lg bg-purple-500/20 px-5 py-2.5 text-lg font-semibold text-white transition-colors duration-200 hover:bg-purple-600"
>
    Profile
</Link>
              <button
                onClick={logout}
                className="rounded-lg bg-red-600 px-5 py-2.5 text-lg font-semibold text-white shadow-sm transition-opacity hover:bg-red-700"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
  href="/login"
  className="rounded-lg bg-purple-500/20 px-5 py-2.5 text-lg font-semibold text-white transition-colors duration-200 hover:bg-purple-600"
>
  Login
</Link>


              <Link
                href="/register"
                className="rounded-lg bg-primary px-5 py-2.5 text-lg font-semibold text-white shadow-sm transition-colors hover:bg-primary-hover"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;




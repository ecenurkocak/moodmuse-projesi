import type { Metadata } from "next";
// import { Inter } from "next/font/google"; // GEÇİCİ OLARAK DEVRE DIŞI BIRAKILDI
import "./globals.css";
import Navbar from "@/components/navbar";
import Footer from "@/components/footer";
import { AuthProvider } from "@/context/AuthContext";

// const inter = Inter({ subsets: ["latin"] }); // GEÇİCİ OLARAK DEVRE DIŞI BIRAKILDI

export const metadata: Metadata = {
  title: "MoodMuse",
  description: "AI-powered mood analysis and suggestion platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`flex flex-col min-h-screen`}>
        <AuthProvider>
          <Navbar />
          <main className="flex-grow container mx-auto px-4 py-8">
            {children}
          </main>
          <Footer />
        </AuthProvider>
      </body>
    </html>
  );
}

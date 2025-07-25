"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";

interface User {
  id: number;
  username: string;
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  loading: boolean;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true); // Başlangıçta yükleme durumunu true yap
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const decodedToken: { sub: string; user_id: number } = jwtDecode(token);
        setUser({ id: decodedToken.user_id, username: decodedToken.sub });
        setIsAuthenticated(true);
      } catch (error) {
        console.error("Invalid token:", error);
        localStorage.removeItem("token");
        setUser(null);
        setIsAuthenticated(false);
      }
    }
    setLoading(false); // Kontrol tamamlandığında yüklemeyi bitir
  }, []);

  const login = (token: string) => {
    localStorage.setItem("token", token);
    try {
      const decodedToken: { sub: string; user_id: number } = jwtDecode(token);
      setUser({ id: decodedToken.user_id, username: decodedToken.sub });
      setIsAuthenticated(true);
    } catch (error) {
      console.error("Invalid token on login:", error);
      // Hatalı token durumunda kullanıcı bilgisi ve kimlik doğrulama durumu sıfırlanır
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setIsAuthenticated(false);
    router.push("/");
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}; 
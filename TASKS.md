### **MoodMuse Projesi Görev Listesi**

#### **Faz 1: Proje Kurulumu, Altyapı ve Temel Ayarlar (Foundation & Setup)**

Bu faz, projenin temelini atmak ve geliştirme ortamını hazırlamak içindir.

*   **1.1. Proje Yönetimi ve Ortam Kurulumu**
    *   [ ] Git repository oluşturma (GitHub, GitLab vb.).
    *   [x] Proje için `backend` ve `frontend` adında iki ana klasör oluşturma.
    *   [x] `README.md` dosyasını ilk proje tanımıyla oluşturma.

*   **1.2. Arka Uç (Backend) Altyapısı - FastAPI**
    *   [x] `backend` klasöründe Python sanal ortamı (virtual environment) oluşturma.
    *   [x] FastAPI ve Uvicorn'u kurma (`pip install fastapi uvicorn`).
    *   [x] Temel "Merhaba Dünya" FastAPI uygulamasını `main.py` içinde oluşturma.
    *   [x] Gerekli bağımlılıklar için `requirements.txt` dosyası oluşturma.

*   **1.3. Ön Yüz (Frontend) Altyapısı - Next.js**
    *   [x] `frontend` klasöründe Next.js projesi oluşturma (`npx create-next-app@latest`).
    *   [x] Proje için temel klasör yapısını düzenleme (components, styles, pages vb.).
    *   [x] TailwindCSS'i projeye entegre etme.

*   **1.4. Veritabanı Kurulumu - SQLite (Değiştirildi)**
    *   [x] PostgreSQL yerine geliştirme kolaylığı için SQLite'a geçildi.
    *   [x] `moodmuse.db` adında veritabanı dosyası oluşturuldu.
    *   [x] Veritabanı bağlantısı `backend/.env` dosyası üzerinden yapılandırıldı.

*   **1.5. Yapay Zeka Servisi**
    *   [ ] Duygu analizi ve metin üretimi için kullanılacak AI modelini seçme (HuggingFace, OpenAI vb.).
    *   [ ] Seçilen servis için API anahtarlarını temin etme.

#### **Faz 2: Arka Uç (Backend) - Temel API Geliştirmesi**

Bu faz, uygulamanın temel mantığını ve veritabanı işlemlerini içerir.

*   **2.1. Veritabanı Modelleri ve Bağlantısı**
    *   [x] FastAPI projesine veritabanı bağlantı konfigürasyonunu ekleme.
    *   [x] SQLAlchemy ve aiosqlite kurulumu.
    *   [x] PRD'deki `Users`, `MoodEntries`, `Suggestions` tabloları için veritabanı modellerini (schema) oluşturma.
    *   [x] Veritabanı tablolarını oluşturacak bir başlangıç script'i yazma.

*   **2.2. Kullanıcı Kimlik Doğrulama (Authentication)**
    *   [x] `POST /api/v1/auth/register` endpoint'ini oluşturma.
    *   [x] Kullanıcı şifrelerini güvenli bir şekilde hash'leme (passlib kullanımı).
    *   [x] `POST /api/v1/auth/login` endpoint'ini oluşturma.
    *   [x] Başarılı girişte JWT (JSON Web Token) üretme.
    *   [ ] Token doğrulaması yapacak bir middleware veya dependency oluşturma.

*   **2.3. Ana İşlevsellik: Duygu Analizi ve Öneri Oluşturma**
    *   [x] `POST /api/v1/analyze` endpoint'ini (korumalı) oluşturma.
    *   [x] Endpoint'in kullanıcıdan bir metin girdisi almasını sağlama.
    *   [x] Seçilen AI servisine bağlanarak gelen metnin duygu analizini yapma (`mood_label`).
    *   [x] Analiz edilen duyguya göre öneri üreten alt fonksiyonlar yazma:
        *   [x] `generate_color_palette(mood)`: Duyguya göre renk paleti döndürür.
        *   [x] `get_spotify_playlist(mood)`: Duyguya uygun Spotify listesi URL'si döndürür.
        *   [x] `generate_inspirational_quote(mood)`: Duyguya uygun ilham verici söz üretir (AI veya hazır liste).
    *   [x] Kullanıcının girdisini `MoodEntries` tablosuna kaydetme.
    *   [x] Oluşturulan öneriyi `Suggestions` tablosuna kaydetme.
    *   [x] Sonuçları kullanıcıya JSON formatında döndürme.

#### **Faz 3: Ön Yüz (Frontend) - Arayüz Geliştirmesi**

Bu faz, kullanıcının etkileşime gireceği arayüzlerin geliştirilmesini kapsar.

*   **3.1. Temel Sayfa ve Bileşenlerin (Component) Oluşturulması**
    *   [ ] Ana layout (Navbar, Footer vb.) bileşenini oluşturma.
    *   [ ] **Kayıt Ol (Register)** sayfası arayüzünü tasarlama (form elemanları).
    *   [ ] **Giriş Yap (Login)** sayfası arayüzünü tasarlama (form elemanları).
    *   [ ] **Ana Sayfa (Dashboard)** arayüzünü tasarlama:
        *   [ ] Duygu metninin girileceği bir `textarea` ve `button`.
        *   [ ] Önerilerin gösterileceği bir alan.

*   **3.2. Öneri Görüntüleme Bileşeni**
    *   [ ] `SuggestionCard` adında bir bileşen oluşturma.
    *   [ ] Renk paletini görsel olarak gösterecek bir alan tasarlama.
    *   [ ] Spotify listesini gömülebilir (embed) bir formatta gösterme.
    *   [ ] İlham verici sözü gösterme.

*   **3.3. Yönlendirme (Routing)**
    *   [ ] Next.js'te `/`, `/login`, `/register`, `/dashboard` sayfaları için yönlendirmeleri ayarlama.
    *   [ ] Korumalı sayfalar için (ör. `/dashboard`) yönlendirme mantığı ekleme (giriş yapılmamışsa `/login`'e yönlendir).

#### **Faz 4: Entegrasyon ve Ek Özellikler**

Bu faz, ön yüz ve arka yüzü birleştirip ek özellikleri tamamlamayı hedefler.

*   **4.1. API Entegrasyonu**
    *   [ ] Frontend'de API istekleri için bir servis katmanı oluşturma (`axios` veya `fetch`).
    *   [ ] Kayıt formunu `POST /api/v1/auth/register` endpoint'ine bağlama.
    *   [ ] Giriş formunu `POST /api/v1/auth/login` endpoint'ine bağlama.
    *   [ ] JWT token'ı frontend'de güvenli bir şekilde saklama (localStorage veya httpOnly cookie).
    *   [ ] Ana sayfadaki duygu giriş formunu `POST /api/v1/analyze` endpoint'ine bağlama.
    *   [ ] API'den dönen öneri verilerini `SuggestionCard` bileşeninde gösterme.

*   **4.2. Geçmiş Görüntüleme Özelliği**
    *   [ ] **Backend:** `GET /api/v1/history` endpoint'ini oluşturma (kullanıcının geçmiş tüm girdilerini ve önerilerini döner).
    *   [ ] **Frontend:** `/history` adında yeni bir sayfa oluşturma.
    *   [ ] **Frontend:** Bu sayfada `GET /api/v1/history` endpoint'inden gelen verileri listeleyerek gösterme.

*   **4.3. Kullanıcı Deneyimi İyileştirmeleri**
    *   [ ] API istekleri sırasında yükleniyor (loading) animasyonları ekleme.
    *   [ ] Hata durumları için kullanıcıya bilgilendirici mesajlar gösterme (Toast, Alert vb.).
    *   [ ] Mobil cihazlar için responsive tasarımı test etme ve iyileştirme.

#### **Faz 5: Test, Dağıtım (Deployment) ve Son Dokunuşlar**

Bu faz, projenin canlıya alınmaya hazırlanmasını içerir.

*   **5.1. Test Süreçleri**
    *   [ ] **Backend:** API endpoint'leri için birim (unit) ve entegrasyon testleri yazma (Pytest).
    *   [ ] **Frontend:** Önemli bileşenler için testler yazma (Jest, React Testing Library).
    *   [ ] Ana kullanıcı akışını (kayıt -> giriş -> öneri alma) baştan sona manuel olarak test etme.

*   **5.2. Dağıtıma Hazırlık (Deployment)**
    *   [ ] Backend için bir Dockerfile oluşturma.
    *   [ ] Frontend için bir Dockerfile oluşturma.
    *   [ ] Tüm servisleri (backend, frontend, db) bir arada çalıştırmak için `docker-compose.yml` dosyası hazırlama.
    *   [ ] Gerekli ortam değişkenlerini (`.env` dosyası) yönetme (veritabanı URL'si, API anahtarları vb.).

*   **5.3. Canlıya Alma**
    *   [ ] Frontend için Vercel veya Netlify gibi bir platform seçme.
    *   [ ] Backend ve veritabanı için Render, Heroku veya bir VPS (DigitalOcean, AWS) seçme.
    *   [ ] Projeyi seçilen platformlara dağıtma.
    *   [ ] HTTPS için SSL sertifikasını yapılandırma.
    *   [ ] Proje dokümantasyonunu (README) güncelleme. 
# 🎨 MoodMuse – Ruh Haline Göre İlham Uygulaması

**MoodMuse**, ruh haline göre kullanıcıya renk paletleri, müzik önerileri ve ilham verici içerikler sunan bir yapay zekâ destekli web uygulamasıdır.

## 💡 Temel Özellikler
- **Hibrit Yapay Zeka Mimarisi:**
    - **Duygu Analizi:** Kullanıcı metinlerinden duygu durumunu tespit etmek için `text-generation-webui` aracılığıyla sunulan yerel bir dil modeli kullanılır.
    - **RAG Destekli Motto Üretimi:** Tespit edilen duyguya özel, **Google Gemini API**'si kullanılarak **kanıt-temelli** ve bağlam açısından zengin mottolar üretilir. Bu sistem, `LangChain` ve `ChromaDB` ile oluşturulmuş bir RAG (Retrieval-Augmented Generation) altyapısı ile güçlendirilmiştir.
- **Kişiselleştirilmiş Öneriler:**
    - 🎨 **Dinamik Renk Paletleri:** `Colormind.io` API'si ile duygu durumuna uygun renk paletleri oluşturulur.
    - 🎵 **Spotify Entegrasyonu:** Kullanıcının ruh haline uygun Spotify çalma listeleri önerilir.
- **Derinlemesine Duygu Kaydı:**
    - 🤔 **"Nedenini Yaz" Özelliği:** Kullanıcılar, o anki ruh hallerinin arkasındaki nedenleri yazarak düşüncelerini kaydedebilir ve `Geçmiş` sayfasında görüntüleyebilir.
    - 😀 **Emoji Etiketleri:** Her duygu kaydına o günü özetleyen bir emoji eklenebilir.
- **Otomasyon & Bildirim:**
    - 💌 `APScheduler` ile haftalık olarak kullanıcıların duygu analizlerini içeren kişiselleştirilmiş e-posta raporları gönderilir.
- **Modern ve Güvenli Altyapı:**
    - 🔐 JWT tabanlı güvenli kullanıcı kimlik doğrulama sistemi.
    - 💾 `SQLite` (Alembic ile yönetilir) ve `ChromaDB` (Vektör) ile veri saklama.
    - 🧩 FastAPI ile oluşturulmuş modüler ve ölçeklenebilir backend yapısı.

| Katman | Teknoloji / Servis | Amaç |
| :--- | :--- | :--- |
| **Frontend** | Next.js (TypeScript) | Kullanıcı arayüzü |
| **Backend** | Python (FastAPI) | API sunucusu ve iş mantığı |
| **Veritabanı**| SQLite, ChromaDB, Alembic | Kullanıcı verileri, vektör depolama ve sürüm kontrolü |
| **AI - Analiz** | `text-generation-webui` | Hızlı duygu tespiti (yerel model) |
| **AI - Üretim** | Google Gemini & RAG | Bağlamla zenginleştirilmiş motto üretimi |
| **AI - RAG** | `LangChain`, `ChromaDB` | Gemini için kanıt ve stil sağlama |
| **Kimlik Doğrulama** | JWT (`python-jose`) | Güvenli kullanıcı oturumları |
| **Otomasyon** | `APScheduler` | Zamanlanmış görevler (haftalık e-posta) |


## 🧠 Yapay Zeka Mimarisi

MoodMuse, üç aşamalı hibrit bir model kullanır:

1.  **Yerel Model (`text-generation-webui`):** Hızlı ve anlık yanıt gerektiren **duygu analizi** görevini üstlenir. Kullanıcının girdiği metnin temel duygusunu (mutlu, üzgün, vb.) anında tespit eder.
2.  **RAG (Retrieval-Augmented Generation):** Bu sistem, `LangChain` ile yönetilir ve `ChromaDB` vektör veritabanında saklanan özel bir bilgi havuzundan (mindfulness, pozitif düşünce gibi konulardaki PDF'ler) ilgili bilgileri çeker. Bu aşamada, tespit edilen duyguya uygun **kanıt metinleri, örnek cümleler ve stil kuralları** toplanır.
3.  **Bulut Tabanlı Model (Google Gemini):** RAG sisteminden gelen zengin bağlam (kanıt, örnekler, stil) ile beslenerek, sıradan bir ilham sözü yerine **daha kaliteli, kanıta dayalı ve kişiselleştirilmiş bir motto** üretir.

Bu üç aşamalı yapı, projenin hem hızlı çalışmasını hem de sıradan metin üretimi yerine derinlikli ve anlamlı çıktılar sunmasını sağlar.

## 🚀 Kurulum ve Çalıştırma

Bu bölüm, projeyi yerel makinenizde kurmak ve çalıştırmak için gereken adımları içerir.

### **1. Projeyi Klonlama**

Öncelikle, projeyi bilgisayarınıza klonlayın:
```bash
git clone https://github.com/ecenurkocak/MoodMuse.git
cd MoodMuse
```

### **2. Ortam Değişkenleri (`.env`)**

Projenin arka ucunun (backend) düzgün çalışabilmesi için ortam değişkenlerini ayarlamanız gerekmektedir. `backend` klasörünün içinde `.env` adında yeni bir dosya oluşturun ve aşağıdaki şablonla doldurun:

```
# Veritabanı Ayarları
DATABASE_URL="sqlite+aiosqlite:///../moodmuse.db"

# JWT Kimlik Doğrulama
SECRET_KEY="jwt_icin_kullanacaginiz_super_gizli_anahtar"

# E-posta Otomasyon Ayarları
SENDER_EMAIL="ornek-mail@gmail.com"
SENDER_PASSWORD="16haneliuygulamasifreniz" # Google App Password

# Yapay Zeka Servisleri
AI_SERVICE_URL="http://127.0.0.1:5000" # text-generation-webui adresi
GEMINI_API_KEY="google_gemini_api_anahtariniz" # Google AI Studio'dan alınan anahtar
```
**Önemli Notlar:**
- `SENDER_PASSWORD` olarak normal Gmail şifrenizi değil, Google Hesap ayarlarınızdan oluşturacağınız **Uygulama Şifresini** kullanmalısınız.
- `GEMINI_API_KEY` değerini Google AI Studio üzerinden almanız gerekmektedir.

### **3. Arka Ucu (Backend) Çalıştırma**

1.  **Python Sanal Ortamı Oluşturma ve Aktifleştirme:**
    ```bash
    # Projenin ana dizinindeyken (capstone/)
    python -m venv venv
    .\venv\Scripts\activate  # Windows için
    # source venv/bin/activate  # macOS/Linux için
    ```

2.  **Gerekli Kütüphaneleri Yükleme:**
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Veritabanını Oluşturma ve Güncelleme:**
    Veritabanı şemasını oluşturmak ve gelecekteki güncellemeleri yönetmek için Alembic kullanılır.
    ```bash
    # Projenin backend dizinindeyken
    cd backend
    alembic upgrade head
    cd .. 
    ```

4.  **RAG Veritabanını Hazırlama (Veri Yükleme):**
    Motto üretimi için kullanılacak kanıt metinlerini işlemeniz gerekir.
    ```bash
    # Projenin ana dizinindeyken
    python -m rag.ingest
    ```
    Bu komut, `rag/source_documents` klasöründeki PDF'leri işleyecek ve `rag/data` klasöründe ChromaDB veritabanını oluşturacaktır.

5.  **Yerel Yapay Zeka Sunucusunu (text-generation-webui) Çalıştırma:**
    Duygu analizi özelliğinin çalışması için yerel dil modelini sunan sunucuyu başlatmanız gerekir. Bu komut, `mistral-7b-instruct-v0.2.Q4_K_M.gguf` modelini otomatik olarak yükleyecektir.
    ```bash
    # Yeni bir terminal açın ve projenin ana dizinindeyken çalıştırın
    cmd /c "cd text-generation-webui && start_windows.bat --model mistral-7b-instruct-v0.2.Q4_K_M.gguf --api --api-port 5000"
    ```
    *Not: Bu sunucunun tamamen başlaması ve modeli yüklemesi birkaç dakika sürebilir.*

6.  **FastAPI Sunucusunu Başlatma:**
    Tüm servisler hazır olduğunda, ana backend sunucusunu başlatın.
    ```bash
    # Projenin ana dizinindeyken
    uvicorn backend.main:app --reload
    ```
    Sunucu artık `http://127.0.0.1:8000` adresinde çalışıyor olmalı.

### **4. Ön Ucu (Frontend) Çalıştırma**

1.  **Gerekli Paketleri Yükleme:**
    ```bash
    # Yeni bir terminal açın ve projenin ana dizinindeyken
    cd frontend
    npm install
    ```

2.  **Next.js Geliştirme Sunucusunu Başlatma:**
    ```bash
    npm run dev
    ```
    Uygulama artık `http://localhost:3000` adresinde çalışıyor olmalı.

## ✨ Katkı Sağla

Pull request ve issue açarak projeye destek olabilirsin.
Geri bildirimler benim için çok değerli! 💌
**Created with 💖 by [@ecenurkocak](https://github.com/ecenurkocak)**


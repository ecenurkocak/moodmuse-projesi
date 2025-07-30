# 🎨 MoodMuse – Ruh Haline Göre İlham Uygulaması

**MoodMuse**, ruh haline göre kullanıcıya renk paletleri, müzik önerileri ve ilham verici içerikler sunan bir yapay zekâ destekli web uygulamasıdır.

## 💡 Özellikler
- 🧠 AI tabanlı ruh hali analizi (Yerel LLM ve `text-generation-webui` ile)
- 🎨 Otomatik tema, renk ve estetik önerileri
- 💌 Haftalık kişiselleştirilmiş e-posta raporları
- 🔐 Kullanıcı girişi (JWT tabanlı kimlik doğrulama)
- 💾 SQLite ile veri saklama
- 🧩 Modüler backend yapısı (FastAPI)

MoodMuse, kullanıcıların mevcut duygularını tanımlayan metinler girmelerine olanak tanır. FastAPI ile güçlendirilmiş arka uç, `text-generation-webui` aracılığıyla sunulan yerel bir dil modelini kullanarak metnin duygusal tonunu analiz eder. Tespit edilen duygu durumuna bağlı olarak, ilham verici sözler, Spotify çalma listeleri ve renk paletleri gibi kişiselleştirilmiş içerikler üretir.

| Katman    | Teknoloji   |
|-----------|-------------|
| **Frontend** | Next.js (TypeScript) |
| **Backend**  | Python (FastAPI) |
| **Veri**     | SQLite |
| **AI Servisi** | `text-generation-webui` |
| **Auth**    | JWT (`python-jose`) |

## 🤖 Otomasyon: Haftalık Duygu Raporu
Proje, kullanıcı etkileşimini artırmak için bir otomasyon ve agent mimarisi içerir.

- **Zamanlanmış Görevler:** `APScheduler` kütüphanesi kullanılarak, her hafta Pazar günleri tüm aktif kullanıcılara e-posta gönderecek bir görev zamanlanmıştır.
- **Veri Analizi:** Bu görev, her kullanıcı için o haftanın en baskın duygu durumunu veritabanından analiz eder.
- **İçerik Üretim Agent'ı:** `LangChain` kütüphanesi kullanılarak oluşturulan bir agent, tespit edilen baskın duyguya göre yerel dil modeline (LLM) bağlanır. Bu agent, kullanıcıya özel ilham verici bir söz ve renk paleti üretir.
- **Kişiselleştirilmiş E-posta:** Üretilen içerikler, `jinja2` ile hazırlanan şık bir HTML şablonuna yerleştirilir ve CSS stilleri `pynliner` ile satır içi hale getirilerek tüm e-posta istemcilerinde mükemmel görünüm sağlanır.

## 🚀 Kurulum ve Çalıştırma

Bu bölüm, projeyi yerel makinenizde kurmak ve çalıştırmak için gereken adımları içerir.

### **1. Projeyi Klonlama**

Öncelikle, projeyi bilgisayarınıza klonlayın:
```bash
git clone https://github.com/ecenurkocak/MoodMuse.git
cd MoodMuse
```

### **2. Ortam Değişkenleri (.env)**

Projenin arka ucunun (backend) düzgün çalışabilmesi için ortam değişkenlerini ayarlamanız gerekmektedir.

1.  `backend` klasörünün içine girin ve `.env.example` adında bir dosya varsa, onu `.env` olarak kopyalayın. Yoksa, `backend` klasörünün içinde elle `.env` adında yeni bir dosya oluşturun.
2.  Oluşturduğunuz `.env` dosyasını aşağıdaki şablonla doldurun:

```
# Veritabanı Ayarları
# Geliştirme için SQLite kullanılıyorsa bu satırı değiştirmeyin.
DATABASE_URL="sqlite+aiosqlite:///../moodmuse.db"

# JWT Kimlik Doğrulama
# Güvenli ve tahmin edilemez bir anahtar belirleyin.
SECRET_KEY="jwt_icin_kullanacaginiz_super_gizli_anahtar"

# E-posta Otomasyon Ayarları
# Haftalık raporları gönderecek olan Gmail hesabının bilgileri.
SENDER_EMAIL="ornek-mail@gmail.com"
# Google'dan alınmış 16 haneli Uygulama Şifresi (App Password).
SENDER_PASSWORD="16haneliuygulamasifreniz"

# Yapay Zeka Servisi (text-generation-webui)
# Oobabooga sunucunuzun çalıştığı adres.
AI_SERVICE_URL="http://127.0.0.1:5000"
```
**Önemli Not:** `SENDER_PASSWORD` olarak normal Gmail şifrenizi değil, Google Hesap ayarlarınızdan oluşturacağınız **Uygulama Şifresini** kullanmalısınız.

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

3.  **Veritabanı Tablolarını Oluşturma:**
    ```bash
    python -m backend.db.create_tables
    ```

4.  **FastAPI Sunucusunu Başlatma:**
    ```bash
    uvicorn backend.main:app --reload
    ```
    Sunucu artık `http://127.0.0.1:8000` adresinde çalışıyor olmalı.

### **4. Ön Ucu (Frontend) Çalıştırma**

1.  **Gerekli Paketleri Yükleme:**
    ```bash
    # Yeni bir terminal açın veya mevcut terminalde devam edin
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

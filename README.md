# 🎨 MoodMuse – Ruh Haline Göre İlham Uygulaması

**MoodMuse**, ruh haline göre kullanıcıya renk paletleri, müzik önerileri ve ilham verici içerikler sunan bir yapay zekâ destekli web uygulamasıdır.

## 💡 Özellikler
- 🧠 AI tabanlı ruh hali analizi (Hugging Face veya OpenAI ile)
- 🎨 Otomatik tema, renk ve estetik önerileri
- 🔐 Kullanıcı girişi (auth sistemi)
- 💾 SQLite ile veri saklama
- 🧩 Modüler backend yapısı (FastAPI veya benzeri)

## ⚙️ Teknoloji Yığını

| Katman    | Teknoloji   |
|-----------|-------------|
| **Frontend** | Next.js (TypeScript) |
| **Backend**  | Python (FastAPI benzeri yapı) |
| **Veri**     | SQLite |
| **AI Servisi** | `ai_service.py` üzerinden çalışıyor |
| **Auth**    | JWT veya token tabanlı yapı (`auth.py`) |

## 📁 Dosya Yapısı

```
frontend/     → Next.js arayüz  
backend/      → Python API ve AI servisi  
  ├── api/    → auth ve analysis endpointleri  
  ├── core/   → AI servis ve config yapısı  
  ├── db/     → CRUD, models ve database işlemleri  
.env          → Ortam değişkenleri  
```

## 🚧 Durum
Şu anda MVP aşamasında. Yakında:
- Kullanıcı geçmişine göre öneri algoritması
- Renk/müzik verilerinin kişiselleştirilmesi
- Takvim entegrasyonu

## 📌 Kurulum

```bash
# Backend
# Bu komutları projenin ana dizininden (capstone/) çalıştırın
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```


## ✨ Katkı Sağla

Pull request ve issue açarak projeye destek olabilirsin.  
Geri bildirimler benim için çok değerli! 💌

**Created with 💖 by [@ecenurkocak](https://github.com/ecenurkocak)**
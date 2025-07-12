## **🎯 Ürün Gereksinimleri Dokümanı (PRD) – _MoodMuse_**

### **1\. Giriş**

**MoodMuse**, kullanıcıların ruh haline göre estetik ve ilham veren öneriler sunan, yapay zeka destekli bir web uygulamasıdır.  
Platformun amacı, özellikle ajanda veya günlük tutan bireylerin ruh haline göre günlerini planlamalarını kolaylaştırmaktır.

Estetik deneyim arayan, yaratıcı kişilere ilham sunmak için geliştirilen MoodMuse, renk paleti, müzik ve motivasyon mesajlarını birleştirerek kullanıcıya duygusal uyum sağlayan öneriler sunar.

### **2\. Amaç ve Hedefler**

**Ana Amaç:  
**Kullanıcının duygu durumunu analiz ederek ona uygun yaratıcı yönlendirmeler (renk, müzik, söz) sağlamak.

**Hedefler:**

- İlk 6 ay içinde 1.000 aktif kullanıcıya ulaşmak.  

- %75 kullanıcı geri dönüşüm oranı sağlamak.  

- Ortalama kullanıcı başına günlük 1 öneri üretimi.  

- İlk 3 ayda en az 3 farklı ruh hali teması geliştirmek.  

### **3\. Kapsam**

**Kapsam Dahilinde:**

- Kullanıcıdan duygu cümlesi alma  

- AI ile duygu analizi yapma  

- Renk paleti önerisi sunma  

- Spotify listesi önermesi  

- Mini ilham mesajı oluşturulması  

- Web arayüzü (masaüstü & mobil uyumlu)  

**Kapsam Dışında:**

- Mobil uygulama (native)  

- Kullanıcılar arası sosyal etkileşim  

### **4\. Sistem Mimarisi ve Bileşenleri**

**Ön Yüz:  
**Next.js kullanılarak geliştirilecek responsive bir arayüz. Kullanıcıdan duygu girişi alınır ve öneriler görsel olarak sunulur.

**Arka Yüz:  
**FastAPI ile geliştirilecek RESTful API, AI servislerine erişim ve duygu analizlerini yönetir.

**Veritabanı:  
**PostgreSQL – kullanıcı verileri, öneri geçmişi ve sistem kayıtları için.

**AI Bileşeni:  
**OpenAI veya HuggingFace tabanlı bir dil modeli ile ruh hali analizi yapılır ve yanıtlar üretilir.

### **5\. İşlevsel Gereksinimler**

- Kullanıcı Girişi / Kayıt  

- Duygu cümlesi alma alanı  

- AI ile analiz ve öneri üretimi  

- Renk paleti çıktısı  

- Spotify liste bağlantısı  

- İlham mesajı üretimi  

- Geçmiş kayıtların görüntülenmesi (isteğe bağlı)  

### **6\. API Gereksinimleri ve Uç Noktaları**

- POST /api/v1/analyze – Kullanıcının ruh halini analiz eder  

- GET /api/v1/suggestions – AI tarafından önerilen içerikleri döner  

- POST /api/v1/auth/register – Kullanıcı kaydı  

- POST /api/v1/auth/login – Giriş işlemi  

- GET /api/v1/history – Kullanıcının önceki girişlerini getirir  

### **7\. İşlevsel Olmayan Gereksinimler**

- **Performans:** Sayfa yüklenme süresi < 2 saniye  

- **Güvenlik:** HTTPS, JWT ile oturum yönetimi  

- **Erişilebilirlik:** Mobil uyumlu, %99 uptime  

- **Uyumluluk:** Chrome, Firefox, Safari, Edge gibi modern tarayıcılarla uyumlu

# MoodMuse Veri Modeli (ER Diyagramı)

Bu doküman, MoodMuse web uygulaması için önerilen veri modeli yapısını içermektedir. Veri modeli, kullanıcıdan alınan duygu girdilerine göre öneriler sunmayı ve geçmişi takip etmeyi amaçlayan bileşenlerden oluşmaktadır.

## Veri Tabanı Tabloları

### Users

| Alan Adı | Veri Türü | Açıklama |
| --- | --- | --- |
| id  | UUID / int | Birincil anahtar |
| email | string | Kullanıcı e-posta adresi |
| password_hash | string | Şifre hash değeri |
| created_at | timestamp | Kayıt tarihi |

### MoodEntries

| Alan Adı | Veri Türü | Açıklama |
| --- | --- | --- |
| id  | UUID / int | Birincil anahtar |
| user_id | foreign key | Users tablosuna bağlı |
| text_input | text | Kullanıcının duygu cümlesi |
| mood_label | string | AI tarafından tahmin edilen duygu |
| created_at | timestamp | Girdi zamanı |

### Suggestions

| Alan Adı | Veri Türü | Açıklama |
| --- | --- | --- |
| id  | UUID / int | Birincil anahtar |
| mood_entry_id | foreign key | MoodEntries tablosuna bağlı |
| color_palette | json / string | Renk paleti |
| spotify_url | string | Spotify çalma listesi |
| quote | string | İlham mesajı |

### History

| Alan Adı | Veri Türü | Açıklama |
| --- | --- | --- |
| id  | UUID / int | Birincil anahtar |
| user_id | foreign key | Users tablosuna bağlı |
| mood_entry_id | foreign key | MoodEntries tablosuna bağlı |
| viewed_at | timestamp | Görüntüleme zamanı |

### Logs (Opsiyonel)

| Alan Adı | Veri Türü | Açıklama |
| --- | --- | --- |
| id  | UUID / int | Birincil anahtar |
| event | string | Olay açıklaması |
| payload | json | İlgili veri |
| timestamp | timestamp | Zaman damgası |
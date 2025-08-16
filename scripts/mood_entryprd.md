Harika bir istek. Bir ürünün en temel özelliğinden başlayarak PRD oluşturmak, geliştirme sürecini daha odaklı ve yönetilebilir hale getirir. Sağladığınız bilgilere dayanarak, sadece MoodMuse'un ana özelliği olan **"Duygu Girişi ve Öneri Akışı"** için detaylı bir özellik PRD'si hazırladım.

---

### **Özellik PRD: Duygu Girişi ve Öneri Akışı**

**Doküman Sürümü:** 1.1
**Tarih:** 26.07.2024
**Özellik Sahibi:** Ürün Yönetimi

### **1. Özellik Özeti ve Amacı**

Bu doküman, MoodMuse uygulamasının temel işlevi olan "Duygu Girişi ve Öneri Akışı" özelliğinin gereksinimlerini tanımlar. Bu özellik, kullanıcının ruh halini belirten bir metin girmesini ve karşılığında anında kişiselleştirilmiş, yaratıcı öneriler (renk paleti, müzik, ilham mesajı) almasını sağlar.

**Amacı:** Kullanıcıya basit ve hızlı bir şekilde değer sunarak ürünün ana vaadini gerçekleştirmek ve kullanıcı etkileşimini başlatmaktır.

### **2. User Stories (Kullanıcı Hikayeleri)**

* **Ana Hikaye:** **Bir MoodMuse kullanıcısı olarak,** gün içinde nasıl hissettiğimi anlatan bir cümle yazmak istiyorum, **böylece** ruh halime uygun, beni anlayan ve bana ilham veren bir renk paleti, müzik listesi ve motivasyon sözü alabilirim.

* **Hata Durumu Hikayesi:** **Bir kullanıcı olarak,** metin kutusunu boş bırakıp butona bastığımda bir uyarı görmek istiyorum, **böylece** ne yapmam gerektiğini anlayabilirim.

* **Bekleme Durumu Hikayesi:** **Bir kullanıcı olarak,** metnimi gönderdikten sonra önerilerim hazırlanırken bir yükleme animasyonu veya mesajı görmek istiyorum, **böylece** sistemin çalıştığını ve beklemem gerektiğini bilirim.

### **3. Fonksiyonel Gereksinimler**

**3.1. Arayüz (Frontend - Next.js)**

* **Giriş Alanı (Text Area):**
    * Anasayfada/giriş ekranında belirgin bir metin giriş alanı bulunmalıdır.
    * İçinde kullanıcıyı yönlendiren bir placeholder metin olmalıdır (Örn: "Bugün nasıl hissediyorsun? Birkaç kelimeyle anlat...").
    * Minimum karakter sınırı 20, maksimum karakter sınırı 300 olarak ayarlanmalıdır. Karakter sayacı olabilir.

* **Gönder Butonu:**
    * Metin giriş alanının altında, eylemi açıkça belirten bir buton bulunmalıdır (Örn: "İlham Bul", "Muse Yarat").
    * Kullanıcı metin girmeden veya minimum karakter sınırına ulaşmadan buton pasif (tıklanamaz) olmalıdır.

* **Yükleme Durumu (Loading State):**
    * Butona tıklandıktan sonra API'den yanıt gelene kadar ekranda bir yükleme göstergesi (spinner, animasyon vb.) gösterilmelidir.
    * Bu sırada ilham verici bir bekleme mesajı gösterilebilir (Örn: "İlham perileri çalışıyor...", "Ruh halin analiz ediliyor...").

* **Öneri Görüntüleme Ekranı:**
    * API'den başarılı yanıt döndüğünde, yükleme ekranı kaybolmalı ve öneriler estetik bir düzende gösterilmelidir.
        * **Renk Paleti:** Renk kodları (HEX) ve renklerin kendisi görsel olarak yan yana gösterilmelidir.
        * **Spotify Listesi:** Tıklanabilir bir bileşen (kart, buton vb.) şeklinde gösterilmeli ve üzerinde "Spotify'da Dinle" gibi bir ifade yer almalıdır. Tıklandığında yeni bir sekmede Spotify URL'si açılmalıdır.
        * **İlham Mesajı:** Okunabilir, büyük bir font ile gösterilmelidir.

**3.2. Arka Uç (Backend - FastAPI)**

* **API Uç Noktası:** `POST /api/v1/analyze`
    * Bu endpoint, kimliği doğrulanmış (authenticated) kullanıcılar tarafından erişilebilir olmalıdır.
    * Gelen isteğin gövdesinde (body) kullanıcının girdiği `text_input` (string) verisi bulunmalıdır.

* **İş Mantığı:**
    1.  Gelen `text_input` verisinin geçerliliği kontrol edilir (boş olmamalı, karakter sınırlarına uymalı).
    2.  Metin, AI Bileşenine (OpenAI/HuggingFace) duygu analizi için gönderilir.
    3.  AI'dan dönen duygu etiketi (`mood_label`, örn: "energetic", "calm") alınır.
    4.  `text_input` ve `mood_label`, ilgili `user_id` ile birlikte `MoodEntries` tablosuna kaydedilir.
    5.  `mood_label`'a göre önceden tanımlanmış veya dinamik olarak üretilen öneriler oluşturulur:
        * **Renk Paleti:** Duyguyla eşleşen bir renk paleti (JSON formatında) seçilir/üretilir.
        * **Spotify URL:** Duyguyla eşleşen bir çalma listesi URL'si seçilir.
        * **İlham Mesajı:** Duyguya uygun bir söz üretilir veya veritabanından seçilir.
    6.  Bu üç öneri, `MoodEntries` girdisine referans verilerek `Suggestions` tablosuna kaydedilir.
    7.  Oluşturulan öneriler (`color_palette`, `spotify_url`, `quote`) API yanıtı olarak kullanıcıya geri döndürülür.

### **4. Kabul Kriterleri (Acceptance Criteria)**

* **Given** kullanıcı giriş yapmış ve anasayfada **When** metin kutusuna "Bugün çok yaratıcı ve enerjik hissediyorum" yazıp "İlham Bul" butonuna tıklar **Then** sistem en fazla 4 saniye içinde enerjik temalı bir renk paleti, bir Spotify linki ve bir ilham sözü göstermelidir.

* **Given** kullanıcı giriş yapmış ve anasayfada **When** metin kutusuna 20 karakterden az metin girer **Then** "İlham Bul" butonu tıklanamaz (disabled) olmalıdır.

* **Given** kullanıcı metni gönderdikten sonra **When** AI servisi yanıt vermezse veya bir hata oluşursa **Then** kullanıcıya "Üzgünüz, şu anda bir sorun oluştu. Lütfen daha sonra tekrar deneyin." gibi bir hata mesajı gösterilmelidir.

* **Given** kullanıcı önerilerini başarıyla aldı **When** veritabanındaki `MoodEntries` ve `Suggestions` tablolarını kontrol eder **Then** yeni bir duygu girdisi ve bu girdiye bağlı bir öneri kaydının oluşturulduğunu görmelidir.

### **5. Kapsam Dışı (Bu Sürüm İçin)**

* Oluşturulan öneriyi düzenleme veya beğenme/beğenmeme.
* Öneriyi sosyal medyada paylaşma.
* Geçmiş önerileri bu ekranda görüntüleme (Bu, ayrı bir "Geçmiş" sayfasının özelliğidir).
* Birden fazla duygu girişi arasında gezinme.

### **6. Bağımlılıklar**

* **Kullanıcı Kimlik Doğrulama (Authentication):** Bu özelliğin çalışması için kullanıcının sisteme giriş yapabilmesi gerekir. `POST /api/v1/auth/login` endpoint'inin çalışır durumda olması şarttır.
* **Harici Servisler:** OpenAI/HuggingFace API'sinin ve Spotify platformunun erişilebilir ve çalışır durumda olması gerekmektedir.
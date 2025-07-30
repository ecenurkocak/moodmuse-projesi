
# Otomasyon ve Agent Mimarisi: Haftalık Duygu Raporu

Bu doküman, MoodMuse projesi kapsamında geliştirilen "Haftalık Duygu Raporu ve İlham Paketi" otomasyonunun teknik detaylarını ve kullanılan agent mimarisini açıklamaktadır.

## 1. Otomasyonun Amacı

Bu otomasyonun temel amacı, kullanıcıların uygulama ile etkileşimini artırmak ve onlara kişiselleştirilmiş bir deneyim sunmaktır. Her hafta, kullanıcının duygu geçmişine dayalı olarak bir özet rapor ve bu rapora uygun olarak üretilmiş ilham verici içerikler (motivasyonel söz, Spotify çalma listesi, renk paleti) e-posta yoluyla gönderilir.

## 2. Otomasyon Süreci

Otomasyon süreci dört ana adımdan oluşur:

1.  **Zamanlama (Scheduling):** `APScheduler` kütüphanesi kullanılarak her Pazar akşamı saat 21:00'de tetiklenen bir görev oluşturulmuştur.
2.  **Veri Analizi:** Zamanlayıcı çalıştığında, veritabanından son 7 gün içinde aktif olan (en az bir duygu girişi yapmış) kullanıcılar çekilir. Her kullanıcı için bu hafta içindeki en baskın duygu (`dominant_mood`) hesaplanır.
3.  **İçerik Üretimi (Agent):** Belirlenen baskın duygu, bir **İçerik Üretim Agent'ına** girdi olarak verilir. Bu agent, duyguya özel olarak kişiselleştirilmiş içerikler üretir.
4.  **E-posta Gönderimi:** Agent tarafından üretilen içerikler (söz, çalma listesi, renk paleti), önceden hazırlanmış bir HTML şablonuna yerleştirilerek kullanıcıya e-posta ile gönderilir.

## 3. Agent Mimarisi

Bu otomasyonda, içerik üretimi için **LangChain** tabanlı bir agent mimarisi kullanılmıştır. Bu agent, belirli bir "duygu" girdisine dayalı olarak çeşitli araçları (Tools) kullanarak anlamlı çıktılar üretir.

-   **Dil Modeli (LLM):** Agent'ın beyni olarak, **`oobabooga/text-generation-webui`** aracılığıyla sunulan yerel bir dil modeli kullanılmaktadır. Bu, OpenAI gibi harici servislere olan bağımlılığı ortadan kaldırır.
-   **Araçlar (Tools):**
    -   `QuoteTool`: Belirtilen duyguya uygun, ilham verici bir söz üretir.
    -   `SpotifyTool`: Duyguya uygun bir Spotify çalma listesi URL'si oluşturur.
    -   `ColorTool`: Duyguyu yansıtan 3 adet HEX renk kodundan oluşan bir palet üretir.
-   **Agent Tipi:** `zero-shot-react-description` agent'ı kullanılarak, LLM'in hangi aracı ne zaman kullanacağına kendisinin karar vermesi sağlanmıştır.

## 4. Kullanılan Teknolojiler ve Kütüphaneler

-   **Backend:** FastAPI
-   **Veritabanı:** PostgreSQL (SQLAlchemy ile)
-   **Agent Mimarisi:** LangChain, text-generation-webui
-   **Zamanlama:** APScheduler
-   **E-posta:** SMTP (Python `smtplib`)

## 5. Örnek Çıktı (Kullanıcıya Giden E-posta)

**Konu: Bu Haftaki Duygu Raporun Hazır!**

Merhaba [Kullanıcı Adı],

İşte bu haftaki duygu özetin:

**Bu hafta en baskın hissettiğin duygu: Neşeli**

Sana özel hazırladığımız ilham paketi:

> "Hayat bisiklete binmek gibidir. Dengenizi korumak için hareket etmeye devam etmelisiniz."

**Haftanın Çalma Listesi:**
[https://spotify.com/mood/joy](https://spotify.com/mood/joy)

**Haftanın Renkleri:**
`#FFD700`, `#FFB347`, `#FF69B4`

Umarız yeni haftaya harika bir başlangıç yaparsın!

Sevgiler,
**MoodMuse Ekibi**

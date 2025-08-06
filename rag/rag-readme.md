# 🧠 MoodMuse Bilgi Bankası (RAG) Mimarisi

Bu doküman, MoodMuse projesinin Retrieval-Augmented Generation (RAG) sisteminin teknik yapısını, işleyişini ve nasıl yönetileceğini açıklamaktadır.

## 🎯 Amaç

Projenin RAG bileşeninin temel amacı, kullanıcılara mindfulness, pozitif psikoloji ve ruh sağlığı gibi konularda güvenilir ve bağlama uygun cevaplar sunan bir "bilgi bankası" oluşturmaktır. Bu sistem, yapay zekanın serbestçe cevap üretmesini engeller; bunun yerine, bizim sağladığımız seçkin dokümanları bir bilgi kaynağı olarak kullanarak daha doğru ve tutarlı yanıtlar vermesini sağlar.

## ⚙️ Mimari ve İşleyiş

Sistemimiz iki ana aşamadan oluşur: **Veri Yükleme (Ingestion)** ve **Sorgulama (Querying)**.


### 1. Veri Yükleme (Ingestion) Aşaması

Bu aşama, `python -m rag.ingest` komutu çalıştırıldığında gerçekleşir ve bilgi bankasını hazırlar.

- **Kaynak Dokümanlar:** Bilgi tabanını oluşturan tüm kaynak PDF dosyaları `rag/source_documents/` klasöründe bulunur.
- **Yükleme (Loading):** `LangChain`'in `PyPDFDirectoryLoader`'ı, bu klasördeki tüm PDF'leri okur.
- **Parçalama (Chunking):** Okunan metinler, `RecursiveCharacterTextSplitter` kullanılarak daha küçük ve anlamsal olarak tutarlı parçalara (chunks) ayrılır. Bu, arama doğruluğunu artırır.
- **Vektörleştirme (Embedding):** Her metin parçası, `HuggingFaceEmbeddings` (spesifik olarak `all-MiniLM-L6-v2` modeli) kullanılarak 384 boyutlu bir vektöre dönüştürülür. Bu vektör, metnin anlamsal özünü temsil eder.
- **Depolama (Storing):** Oluşturulan vektörler ve orijinal metin parçaları, `ChromaDB` vektör veritabanına kaydedilir. Veritabanı dosyaları, `db/chroma/` klasöründe kalıcı olarak saklanır.

### 2. Sorgulama (Querying) Aşaması

Bu aşama, kullanıcı arayüzden bir soru sorduğunda (`/api/v1/rag/query` endpoint'i aracılığıyla) gerçekleşir.

- **Sorgu Vektörleştirme:** Kullanıcının sorduğu soru, aynı embedding modeli (`all-MiniLM-L6-v2`) kullanılarak bir vektöre dönüştürülür.
- **Benzerlik Araması (Retrieval):** `ChromaDB`, kullanıcının sorgu vektörüne en çok benzeyen (anlamsal olarak en ilgili) metin parçalarını veritabanından bulur (`k=2` ayarı ile en ilgili 2 parça alınır).
- **Cevap Üretimi (Generation):**
    - Bulunan ilgili metin parçaları (bağlam/context) ve kullanıcının orijinal sorusu, `rag_chain.py` dosyasında tanımlanan bir prompt şablonuna yerleştirilir.
    - Bu birleştirilmiş metin, cevap üretmesi için `text-generation-webui` aracılığıyla sunulan yerel dil modeline (LLM) gönderilir.
    - LLM, kendisine verilen bağlamı kullanarak soruya en uygun cevabı üretir.

Bu yaklaşım sayesinde, LLM'in "halüsinasyon görmesi" veya konu dışı cevaplar vermesi engellenir ve cevapların bizim sağladığımız kaynaklara dayalı olması sağlanır.

## 🛠️ Teknolojiler ve Bileşenler

- **Orkestrasyon:** `LangChain`
- **Vektör Veritabanı:** `ChromaDB`
- **Embedding Modeli:** `HuggingFaceEmbeddings` (`sentence-transformers/all-MiniLM-L6-v2`)
- **Dil Modeli (LLM):** `text-generation-webui` üzerinden sunulan yerel bir model.
- **API Sunucusu:** `FastAPI`

## ➕ Bilgi Bankasına Yeni Doküman Nasıl Eklenir?

1.  **PDF Ekleme:** Bilgi bankasına eklemek istediğiniz yeni `.pdf` dosyasını `rag/source_documents/` klasörünün içine kopyalayın.
2.  **Veri Yükleme Komutunu Çalıştırma:** Projenin ana dizinindeyken terminali açın ve aşağıdaki komutu çalıştırın:
    ```bash
    python -m rag.ingest
    ```
3.  **İşlem Tamamlandı:** Bu komut, yeni eklediğiniz PDF'i işleyecek, vektörlere dönüştürecek ve `ChromaDB` veritabanına ekleyecektir. Artık RAG sisteminiz, yeni eklediğiniz belgedeki bilgileri kullanarak da cevaplar üretebilir.

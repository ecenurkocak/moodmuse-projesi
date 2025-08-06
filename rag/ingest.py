# rag/ingest.py

import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Sabitleri tanımlayalım
SOURCE_DIRECTORY = 'rag/source_documents'
PERSIST_DIRECTORY = 'db/chroma'
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def main():
    print("="*80)
    print("Ingestion script'i başlatılıyor...")
    
    # Kaynak dizinindeki PDF dosyalarını bul
    pdf_files = glob.glob(os.path.join(SOURCE_DIRECTORY, "*.pdf"))
    
    if not pdf_files:
        print(f"HATA: '{SOURCE_DIRECTORY}' klasöründe hiç PDF dosyası bulunamadı.")
        return
        
    print(f"Bulunan PDF dosyaları: {len(pdf_files)}")
    for f in pdf_files:
        print(f" - {os.path.basename(f)}")
        
    all_documents = []
    print("\nBelgeler yükleniyor...")
    for file_path in pdf_files:
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            print(f" - '{os.path.basename(file_path)}' yüklendi ({len(documents)} sayfa).")
            all_documents.extend(documents)
        except Exception as e:
            print(f"HATA: '{os.path.basename(file_path)}' yüklenirken bir hata oluştu: {e}")
            continue # Bir dosya hatalıysa diğerleriyle devam et

    if not all_documents:
        print("HATA: Hiçbir belge başarıyla yüklenemedi.")
        return

    print(f"\nToplam {len(all_documents)} sayfa yüklendi.")

    print("Belgeler parçalara (chunk) ayrılıyor...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(all_documents)
    
    print(f"Toplam {len(texts)} metin parçası (chunk) oluşturuldu.")

    print("\nEmbedding modeli yükleniyor...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    print(f"'{EMBEDDING_MODEL}' modeli başarıyla yüklendi.")

    print("\nVectorDB (Chroma) oluşturuluyor ve kaydediliyor...")
    if not os.path.exists(PERSIST_DIRECTORY):
        os.makedirs(PERSIST_DIRECTORY)
        print(f"'{PERSIST_DIRECTORY}' klasörü oluşturuldu.")

    db = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    print("\nİşlem tamamlandı! VectorDB oluşturuldu ve kaydedildi.")
    print(f"Veritabanı konumu: '{os.path.abspath(PERSIST_DIRECTORY)}'")
    print("="*80)


if __name__ == "__main__":
    main()

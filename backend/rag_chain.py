# backend/rag_chain.py

"""
Bu modül, LangChain kütüphanesini kullanarak Retrieval-Augmented Generation (RAG) 
zincirini oluşturur ve yönetir.

Ana işlevleri:
1. Gerekli modelleri (embedding ve LLM) yüklemek.
2. Kalıcı bir vektör veritabanından (ChromaDB) bilgiyi çekmek.
3. Kullanıcı sorgularını, bulunan bağlamla birleştirerek cevap üretmek.

Bu modül, "tembel yükleme" (lazy loading) prensibiyle çalışır. Yani, ağır olan
modeller ve RAG zinciri, sunucu başlarken değil, ilk sorgu geldiğinde bir defaya 
mahsus olmak üzere yüklenir.
"""

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# --- Konfigürasyon ve Sabitler ---

# Vektör veritabanının diskteki konumu
PERSIST_DIRECTORY = 'db/chroma'
# text-generation-webui tarafından sağlanan OpenAI uyumlu API'nin adresi
OPENAI_API_BASE = "http://127.0.0.1:5000/v1"
# Metinleri vektörlere dönüştürmek için kullanılacak embedding modeli
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Global Değişkenler ---

# RAG zincirini hafızada tutmak için global değişken.
# Bu, zincirin her istekte yeniden oluşturulmasını engeller.
qa_chain_instance = None


def _initialize_rag_chain():
    """
    RAG zincirini başlatan ve yapılandıran özel fonksiyon.

    Bu fonksiyon, embedding modelini, vektör veritabanını ve LLM'i yükler,
    ardından bunları bir RetrievalQA zinciri içinde birleştirir.
    
    Returns:
        RetrievalQA: Kullanıma hazır RAG zinciri.
    """
    global qa_chain_instance
    
    print("RAG zinciri ilk defa başlatılıyor. Bu işlem biraz zaman alabilir...")

    # Adım 1: Metinleri vektöre çevirecek embedding modelini yükle.
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # Adım 2: Disk'te kalıcı olarak saklanan vektör veritabanını yükle.
    db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)

    # Adım 3: text-generation-webui üzerinden yerel LLM'i yükle.
    llm = ChatOpenAI(
        base_url=OPENAI_API_BASE,
        api_key="sk-",  # API anahtarı zorunlu ama yerel model için kullanılmaz.
        temperature=0.7,
        model_name="local-model"
    )

    # Adım 4: LLM'e nasıl cevap üreteceğini söyleyen talimat şablonunu (prompt) oluştur.
    prompt_template = """
    Sana verilen bağlamı (context) kullanarak kullanıcı sorusuna cevap ver. 
    Eğer cevabı bağlamda bulamazsan, "Bu konuda bilgim yok." de. Cevapların ilham verici ve pozitif olsun.

    BAĞLAM: {context}
    SORU: {question}
    CEVAP:
    """
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # Adım 5: Tüm parçaları birleştirerek RAG zincirini oluştur.
    # "stuff" chain type, bulunan tüm belgeleri tek bir prompt'ta birleştirir.
    # "retriever", veritabanından ilgili belgeleri getiren bileşendir.
    qa_chain_instance = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 2}), # Sorgu başına en ilgili 2 belgeyi getir.
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    print("RAG zinciri başarıyla başlatıldı ve artık kullanıma hazır.")
    return qa_chain_instance


def get_current_chain():
    """
    Mevcut RAG zincirini döndürür. Eğer zincir henüz başlatılmamışsa, başlatır.
    """
    if qa_chain_instance is None:
        return _initialize_rag_chain()
    return qa_chain_instance


async def query_rag_chain(query: str) -> str:
    """
    API endpoint'i tarafından çağrılacak ana fonksiyon.

    Verilen bir sorgu için RAG zincirini asenkron olarak çalıştırır ve
    sadece metin cevabını döndürür.

    Args:
        query: Kullanıcının sorduğu soru.

    Returns:
        LLM tarafından üretilen metin cevabı.
    """
    chain = get_current_chain()
    try:
        result = await chain.ainvoke({"query": query})
        return result.get("result", "Cevap üretilirken bir sorun oluştu.")
    except Exception as e:
        print(f"RAG zinciri sorgulanırken hata oluştu: {e}")
        return "Modelden cevap alınırken bir hata meydana geldi. Lütfen daha sonra tekrar deneyin."

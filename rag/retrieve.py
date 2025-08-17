from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

EMBED = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
DB = Client(Settings(persist_directory="rag/data", anonymized_telemetry=False))
COLL = DB.get_or_create_collection("moodmuse_rag")

def query_similar(text, where=None, k=2):
    """
    ChromaDB'de anlamsal arama yapar. 
    'where' filtresi birden fazla koşul içeriyorsa, bunları $and operatörü ile birleştirir.
    """
    
    final_where = where or {}
    if where and len(where) > 1:
        final_where = {"$and": [{key: value} for key, value in where.items()]}

    emb = EMBED.encode(text).tolist()
    res = COLL.query(query_embeddings=[emb], n_results=k, where=final_where)
    docs = res["documents"][0] if res and res["documents"] else []
    metas = res["metadatas"][0] if res and res["metadatas"] else []
    return list(zip(docs, metas))

def pick_for(emotion:str):
    style = query_similar("kısa yargısız sen kip nefes", where={"type":"style"}, k=1)
    # Birden fazla koşul içeren 'where' filtresi artık doğru çalışacak.
    examples = query_similar(f"{emotion} için kısa örnek", where={"type":"example","emotion":emotion}, k=2)
    evidence = query_similar(f"nefes farkındalık {emotion}", where={"type":"evidence"}, k=1)
    return style, examples, evidence

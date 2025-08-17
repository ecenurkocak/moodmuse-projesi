from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid, glob, os
from pypdf import PdfReader

EMBED = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
DB = Client(Settings(persist_directory="rag/data", anonymized_telemetry=False))
COLL = DB.get_or_create_collection("moodmuse_rag")

def chunk(txt, size=500, overlap=120):
    out=[]; i=0
    while i < len(txt):
        out.append(txt[i:i+size]); i += (size-overlap)
    return out

def extract_text(fp):
    if fp.lower().endswith(".pdf"):
        r = PdfReader(fp); return " ".join([p.extract_text() or "" for p in r.pages])
    # md/txt varsa burada genişlet
    with open(fp, "r", encoding="utf-8", errors="ignore") as f: return f.read()

def add_doc(text, meta):
    for c in chunk(text):
        COLL.add(ids=[str(uuid.uuid4())],
                 documents=[c],
                 metadatas=[meta],
                 embeddings=[EMBED.encode(c).tolist()])

def ingest_folder(path="rag/source_documents"):
    for fp in glob.glob(os.path.join(path, "**/*.*"), recursive=True):
        text = extract_text(fp)
        add_doc(text, {"type":"evidence","emotion":"null","source":os.path.basename(fp)})

if __name__ == "__main__":
    ingest_folder()
    print("Ingest tamam ✅")

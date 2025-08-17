harika—o zaman senin mimarine göre (⟨LLM yalnızca 8 duyguya sınıflar⟩ → ⟨RAG bağlam/snippet toplar⟩ → ⟨Gemini tek prompt’la yanıt üretir⟩) sıfırdan bir **`rag/README.md`** taslağı hazırlıyorum. Bunu repo’ya aynen koyabilirsin.

---

# RAG (Retrieval-Augmented Generation) — MoodMuse

LLM sadece duygu sınıflıyor (**mutlu, üzgün, kızgın, şaşkın, sakin, enerjik, düşünceli, kararsız**).
**RAG**, Gemini’ye giden prompt’u “bağlamla” güçlendirir: yazım stili, duygu-özel örnek ve **kanıt snippet’i** (PDF’lerden) ekler. Böylece Gemini’nın cümlesi “havada kalmaz”, kanıta ve duyguya göre hedeflenir. PRD’deki “mini ilham mesajı” tam olarak bu modülle beslenecek.

## 0) Bu modül projenin neresinde?

```
[Kullanıcı metni] 
      │
      ▼
[DUYGU Sınıflandırma LLM] ──► label ∈ {8 mood}
      │
      ▼
[RAG Seçici]
  • Stil kuralları (kısa, yargısız, “sen”)
  • Duyguya uygun örnek cümle(ler)
  • PDF’lerden 1–2 cümlelik kanıt snippet’i
      │
      ▼  (tek prompt)
[Gemini Üretici] ──► 1 cümlelik motto (≤18 kelime, mini ritüel)
```

> Kaynak PDF’ler `rag/source_documents/` altında: Mindfulness, Pozitif Düşünme, Renkler vb. (repo yapında zaten listelenmiş).

---

## 1) Klasör yapısı

```
project-root/
  rag/
    README.md               # bu dosya
    source_documents/       # PDF/MD kaynaklar (mindfulness, renkler, pozitif düşünme…)
    data/                   # Chroma kalıcılık dizini
    ingest.py               # belge → chunk → embedding → vektör DB
    retrieve.py             # duyguya ve tipe göre parçaları getirir
    prompt_builder.py       # RAG çıktısını Gemini tek prompt’una diker
```

> Capstone tesliminde “rag/ klasöründe çalışan sistem + rag-readme.md” açıkça istenir.

---

## 2) İçerik modelimiz (parça tipleri)

Her parça **200–500 karakter**, **tek fikir** ve şu metadata ile tutulur:

* `type`: `"style"` (yazım rehberi) | `"example"` (duygu-özel mini cümle) | `"evidence"` (PDF’ten kanıt)
* `emotion`: `mutlu|üzgün|kızgın|şaşkın|sakin|enerjik|düşünceli|kararsız|null`
* `source`: dosya adı/başlığı (örn. `Mindfulness ile Stres yönetimi.pdf`)

**Örnekler**

* `style`: “Kısa, yargısız; ‘sen/sana’ kipinde; **tek** mini ritüel; ≤18 kelime.”
* `example (kaygılı≈şaşkın)`: “Bir an dur; üç derin nefesle zemini yeniden hissediyorsun.”
* `evidence`: “Yavaş ve düzenli nefes, kısa sürede bedensel gerginliği azaltmaya yardımcı olabilir.” (Mindfulness)

---

## 3) Ingestion (tek seferlik içe aktarma)

Amaç: `rag/source_documents/` içeriğini küçük parçalara bölüp embedding’leyerek **Chroma**’ya yazmak.

Kurulum:

```
pip install chromadb sentence-transformers pypdf
```

`rag/ingest.py` (özet taslak):

```python
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
        add_doc(text, {"type":"evidence","emotion":None,"source":os.path.basename(fp)})

if __name__ == "__main__":
    ingest_folder()
    print("Ingest tamam ✅")
```

---

## 4) Retrieval (üretim öncesi hangi parçaları çekiyoruz?)

Motto üretirken hedef set:

* **1 × `style`** (evrensel yazım kuralı)
* **1–2 × `example`** (duyguya uygun)
* **1 × `evidence`** (mindfulness/pozitif düşünme/renkler pdf’lerinden kanıt)

`rag/retrieve.py` (özet):

```python
from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

EMBED = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
DB = Client(Settings(persist_directory="rag/data", anonymized_telemetry=False))
COLL = DB.get_or_create_collection("moodmuse_rag")

def query_similar(text, where=None, k=2):
    emb = EMBED.encode(text).tolist()
    res = COLL.query(query_embeddings=[emb], n_results=k, where=where or {})
    docs = res["documents"][0] if res and res["documents"] else []
    metas = res["metadatas"][0] if res and res["metadatas"] else []
    return list(zip(docs, metas))

def pick_for(emotion:str):
    style = query_similar("kısa yargısız sen kip nefes", where={"type":"style"}, k=1)
    examples = query_similar(f"{emotion} için kısa örnek", where={"type":"example","emotion":emotion}, k=2)
    evidence = query_similar(f"nefes farkındalık {emotion}", where={"type":"evidence"}, k=1)
    return style, examples, evidence
```

> Capstone yönergesi: “Chunking + VectorDB (Chroma/FAISS) + basit arama → özelliğe ekle.”

---

## 5) Prompt-conditioning (Gemini tek prompt şablonu)

`rag/prompt_builder.py` (özet):

```python
PROMPT = """
ROL: Sen bir “motto yazarı”sın. 
Amaç: Kullanıcının duygu ifadesine uygun, KISA, yargısız, "sen" kipinde, 
tek mini ritüel içeren 1 cümle üret.

STİL KURALI:
{style}

ÖRNEKLER:
- {ex1}
- {ex2}

KANIT:
- {evidence} (Kaynak: {source})

GİRDİ:
Duygu: {emotion}
Metin: "{user_text}"

KISIT:
- Türkçe yaz.
- En fazla 18 kelime.
- Yargısız ol; “hemen yap” tonu verme.
- En az bir nefes/mini ritüel/küçük eylem öner.

İSTENEN ÇIKTI (yalnızca tek cümle):
<motto>
""".strip()

def build_prompt(user_text, emotion, style, examples, evidence):
    s = style[0][0] if style else "- Kısa, yargısız; sen/sana; mini ritüel; ≤18 kelime."
    ex1 = (examples[0][0] if examples else "Bugün iki derin nefes iyi gelir.")
    ex2 = (examples[1][0] if len(examples)>1 else "Kendine nazik ol; küçük bir adım yeter.")
    ev_text, ev_meta = (evidence[0][0], evidence[0][1]) if evidence else ("Yavaş, ritimli nefes gerginliği azaltabilir.","(genel)")
    return PROMPT.format(style=s, ex1=ex1, ex2=ex2,
                         evidence=ev_text, source=ev_meta.get("source","(yok)"),
                         emotion=emotion, user_text=user_text[:280])
```

---

## 6) Entegrasyon akışı (senin mimarine göre)

1. **Sınıflandırıcı LLM**
   `label = classify(user_text)  # mutlu|üzgün|kızgın|şaşkın|sakin|enerjik|düşünceli|kararsız`

2. **RAG**
   `style, examples, evidence = pick_for(label)`
   `prompt = build_prompt(user_text, label, style, examples, evidence)`

3. **Gemini**
   `motto = gemini.generate(prompt)  # tek çağrı`

> Not: PRD’de tanımlı “mini ilham mesajı” çıktısı doğrudan bu akıştan gelir.

---

## 7) Kalite kontrol (otomatik/minik)

* **Tek cümle** ve **≤18 kelime** mi?
* “**sen/sana**” kipinde mi?
* **Mini ritüel** var mı (nefes/grounding/küçük adım)?
* **Yargısız** mı (zorundasın, mecbursun, “hemen” yok)?
* **Kaynak adı** (evidence.source) loglanıyor mu (şeffaflık)?

---

## 8) API önerisi

`POST /api/v1/motto` → body: `{ user_text, emotion }`

* `emotion` doğrudan sınıflandırıcıdan geliyor.
* Backend: retrieval → prompt → Gemini → `{"motto": "...", "used": {emotion, style, evidence, source}}`

---

## 9) Güncelleme & bakım

* Yeni PDF ekledin → `rag/source_documents/` → `python rag/ingest.py`
* Stil/örnek setini değiştirdin → `type:"style"/"example"` belgelerini güncelle → ingest.
* İleride istersen CSV tabanlı “konfig” katmanı ekleyip vektör yerine doğrudan lookup yapabilirsin.

---

## 10) Sık hatalar

* **Chunk’lar çok büyük/küçük** → 200–500 karakter idealdir.
* **Metadata eksik** → `type`/`emotion` olmadan yanlış parçalar gelir.
* **Prompt uzun ve muğlak** → kısıtları net yaz (tek cümle, ≤18 kelime, “sen”, mini ritüel).
* **Kanıt didaktik** → 1–2 cümle, yumuşak ton.

---

### Kaynak/bağlam notları

* Capstone’daki RAG adımı: “Chunking + VectorDB (Chroma/FAISS) + çalışan `rag/` sistemi + README” şartı.
* Repo’da hâlihazırda mindfulness/renk/pozitif düşünme PDF’leri mevcut.

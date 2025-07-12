# Hugging Face MCP Tool & Server

Bu proje, Hugging Face modelleri ile etkileşim kurmak için hem komut satırı aracı hem de MCP (Model Context Protocol) server içerir.

## 📁 Dosya Yapısı

```
capstone/
├── hf_mcp_tool.py          # Komut satırı aracı
├── hf_mcp_server.py        # MCP Server
├── mcp_server_config.json  # Server konfigürasyonu
├── test_mcp_client.py      # Test client
├── start_server.bat        # Windows server başlatma
├── start_server.sh         # Linux/Mac server başlatma
├── test_server.bat         # Windows test script
├── test_server.sh          # Linux/Mac test script
├── requirements.txt        # Python bağımlılıkları
└── README.md              # Bu dosya
```

## 🚀 Kurulum

```bash
pip install -r requirements.txt
```

**Not:** İlk kurulumda `transformers`, `torch` ve diğer kütüphaneler otomatik olarak yüklenecektir. Bu işlem biraz zaman alabilir.

## 🔧 Kullanım

### 1. Token Ayarlama (İsteğe bağlı)
Eğer özel modeller kullanacaksan, Hugging Face token'ınızı ayarlayın:

```bash
# Windows
set HF_TOKEN=hf_your_token_here

# Linux/Mac
export HF_TOKEN=hf_your_token_here
```

### 2. Komut Satırı Aracı

#### Popüler modelleri listele:
```bash
python hf_mcp_tool.py --list
```

#### Model bilgisi al:
```bash
python hf_mcp_tool.py --info gpt2
```

#### Inference yap:
```bash
python hf_mcp_tool.py --infer gpt2 "Hello world"
```

### 3. MCP Server

#### Server'ı başlat:
```bash
# Windows
start_server.bat

# Linux/Mac
chmod +x start_server.sh
./start_server.sh
```

#### Server'ı test et:
```bash
# Windows
test_server.bat

# Linux/Mac
chmod +x test_server.sh
./test_server.sh
```

#### Manuel test:
```bash
# Health check
curl http://localhost:3000/health

# List models
curl http://localhost:3000/models

# Inference (API)
curl -X POST http://localhost:3000/inference \
  -H "Content-Type: application/json" \
  -d '{"model_id": "gpt2", "inputs": "Hello world"}'

# Inference (Local - requires transformers/torch)
curl -X POST http://localhost:3000/inference \
  -H "Content-Type: application/json" \
  -d '{"model_id": "gpt2", "inputs": "Hello world", "use_local": true}'
```

## 📋 API Endpoints

- `GET /health` - Server durumu
- `GET /models` - Mevcut modeller
- `POST /inference` - Model inference (API veya Local)

### Inference Parameters:
- `model_id` (required): Model adı
- `inputs` (required): Girdi metni
- `use_local` (optional): Yerel çalıştırma için `true` (transformers/torch gerekli)

## 🧪 Test Örnekleri

```bash
# Text generation
python hf_mcp_tool.py --infer gpt2 "The future of AI is"

# Sentiment analysis
python hf_mcp_tool.py --infer distilbert-base-uncased-finetuned-sst-2-english "I love this movie!"

# Translation
python hf_mcp_tool.py --infer t5-small "translate English to French: Hello world"
```

## 🔧 Konfigürasyon

`mcp_server_config.json` dosyasında server ayarlarını değiştirebilirsin:

```json
{
  "mcpServers": {
    "huggingface-mcp": {
      "command": "python",
      "args": ["hf_mcp_server.py"],
      "env": {
        "HF_TOKEN": "${HF_TOKEN}",
        "MCP_SERVER_PORT": "3000"
      }
    }
  }
}
```

## 📊 Desteklenen Model Türleri

- Text Generation (GPT-2, DialoGPT)
- Text Classification (BERT, DistilBERT)
- Translation (T5, mT5)
- Summarization (BART, T5)
- Question Answering (BERT variants)

## 🐛 Sorun Giderme

1. **Server başlamıyor**: Python ve requests kütüphanesinin yüklü olduğundan emin ol
2. **Inference hatası**: HF_TOKEN'ın doğru ayarlandığından emin ol
3. **Port çakışması**: `MCP_SERVER_PORT` environment variable'ını değiştir 
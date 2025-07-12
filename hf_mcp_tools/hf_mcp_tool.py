import requests
import argparse
import os

MCP_URL = "https://api-inference.huggingface.co"
HF_TOKEN = os.getenv("HF_TOKEN")  # Ortam değişkeninden token al

def get_headers():
    headers = {}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"
    return headers

def list_models():
    """Hugging Face'deki popüler modelleri listeler"""
    popular_models = [
        "gpt2", "bert-base-uncased", "distilbert-base-uncased",
        "microsoft/DialoGPT-medium", "facebook/bart-base",
        "t5-small", "google/flan-t5-small"
    ]
    print("Popüler Hugging Face Modelleri:")
    for model in popular_models:
        print(f"- {model}")

def get_model_info(model_id):
    """Model hakkında bilgi alır"""
    url = f"https://huggingface.co/api/models/{model_id}"
    response = requests.get(url)
    if response.status_code == 200:
        model_info = response.json()
        print(f"Model: {model_id}")
        print(f"Downloads: {model_info.get('downloads', 'N/A')}")
        print(f"Likes: {model_info.get('likes', 'N/A')}")
        print(f"Tags: {', '.join(model_info.get('tags', []))}")
    else:
        print(f"Model bilgisi alınamadı: {response.status_code}")

def run_inference(model_id, input_text):
    """Model ile inference yapar"""
    url = f"{MCP_URL}/models/{model_id}"
    payload = {"inputs": input_text}
    response = requests.post(url, json=payload, headers=get_headers())
    if response.status_code == 200:
        result = response.json()
        print("Çıktı:")
        if isinstance(result, list) and len(result) > 0:
            if 'generated_text' in result[0]:
                print(result[0]['generated_text'])
            elif 'label' in result[0]:
                print(f"Label: {result[0]['label']}, Score: {result[0]['score']:.4f}")
            else:
                print(result)
        else:
            print(result)
    else:
        print(f"Inference başarısız: {response.status_code}")
        print(f"Hata: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hugging Face MCP Tool")
    parser.add_argument("--list", action="store_true", help="Popüler modelleri listele")
    parser.add_argument("--info", type=str, help="Model bilgisi al (model_id)")
    parser.add_argument("--infer", nargs=2, metavar=("MODEL_ID", "INPUT"), help="Inference yap")

    args = parser.parse_args()

    if args.list:
        list_models()
    elif args.info:
        get_model_info(args.info)
    elif args.infer:
        run_inference(args.infer[0], args.infer[1])
    else:
        parser.print_help() 
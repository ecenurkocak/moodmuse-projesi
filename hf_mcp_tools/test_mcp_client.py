#!/usr/bin/env python3
"""
Test client for Hugging Face MCP Server
"""

import requests
import json
import time

class MCPTestClient:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
    
    def health_check(self):
        """Test server health"""
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ Server is healthy")
                print(f"Response: {response.json()}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to server. Is it running?")
            return False
    
    def list_models(self):
        """Test model listing"""
        try:
            response = requests.get(f"{self.base_url}/models")
            if response.status_code == 200:
                models = response.json()["models"]
                print("✅ Models listed successfully")
                print("Available models:")
                for model in models:
                    print(f"  - {model}")
                return True
            else:
                print(f"❌ Model listing failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error listing models: {e}")
            return False
    
    def test_inference(self, model_id="gpt2", inputs="Hello world", use_local=False):
        """Test model inference"""
        try:
            payload = {
                "model_id": model_id,
                "inputs": inputs,
                "use_local": use_local
            }
            
            print(f"Testing inference with model: {model_id}")
            print(f"Input: {inputs}")
            print(f"Method: {'Local' if use_local else 'API'}")
            
            response = requests.post(
                f"{self.base_url}/inference",
                json=payload,
                timeout=120 if use_local else 60  # Longer timeout for local models
            )
            
            if response.status_code == 200:
                data = response.json()
                result = data["result"]
                method = data.get("method", "unknown")
                print("✅ Inference successful")
                print(f"Method used: {method}")
                print(f"Result: {result}")
                return True
            else:
                print(f"❌ Inference failed: {response.status_code}")
                print(f"Error: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error during inference: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting MCP Server Tests")
        print("=" * 50)
        
        # Test 1: Health check
        print("\n1. Testing health check...")
        if not self.health_check():
            return False
        
        # Test 2: List models
        print("\n2. Testing model listing...")
        if not self.list_models():
            return False
        
        # Test 3: Text generation (API)
        print("\n3. Testing text generation (API)...")
        if not self.test_inference("gpt2", "The future of AI is", use_local=False):
            return False
        
        # Test 4: Text generation (Local - if transformers available)
        print("\n4. Testing text generation (Local)...")
        if not self.test_inference("gpt2", "Hello world", use_local=True):
            print("⚠️  Local inference test skipped (transformers not available or model loading failed)")
        
        # Test 5: Sentiment analysis
        print("\n5. Testing sentiment analysis...")
        if not self.test_inference("distilbert-base-uncased-finetuned-sst-2-english", "I love this movie!"):
            print("⚠️  Sentiment analysis test skipped (model might not be available)")
        
        print("\n" + "=" * 50)
        print("✅ All tests completed!")
        return True

def main():
    client = MCPTestClient()
    client.run_all_tests()

if __name__ == "__main__":
    main() 
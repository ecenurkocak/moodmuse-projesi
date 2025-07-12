#!/usr/bin/env python3
"""
Hugging Face MCP Server
Model Context Protocol server for Hugging Face models
"""

import json
import logging
import os
import sys
import time
from typing import Dict, Any, List
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Import transformers and torch for local model inference
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification
    from transformers.pipelines import pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: transformers/torch not available. Only API inference will work.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MCPHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.hf_token = os.getenv("HF_TOKEN")
        self.api_url = "https://api-inference.huggingface.co"
        self.local_models = {}  # Cache for loaded local models
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == "/health":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "healthy", "timestamp": time.time()}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == "/models":
            self.list_models()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == "/inference":
            self.handle_inference()
        else:
            self.send_response(404)
            self.end_headers()
    
    def list_models(self):
        """List available models"""
        models = [
            "gpt2", "bert-base-uncased", "distilbert-base-uncased",
            "microsoft/DialoGPT-medium", "facebook/bart-base",
            "t5-small", "google/flan-t5-small"
        ]
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"models": models}
        self.wfile.write(json.dumps(response).encode())
    
    def load_local_model(self, model_id):
        """Load a model locally using transformers"""
        if not TRANSFORMERS_AVAILABLE:
            return None
            
        if model_id in self.local_models:
            return self.local_models[model_id]
        
        try:
            logger.info(f"Loading model locally: {model_id}")
            
            # Try to determine model type and load appropriate pipeline
            if "gpt" in model_id.lower() or "dialo" in model_id.lower():
                # Text generation model
                pipe = pipeline("text-generation", model=model_id, device="cpu")
            elif "bert" in model_id.lower() or "distilbert" in model_id.lower():
                # Text classification model
                pipe = pipeline("text-classification", model=model_id, device="cpu")
            elif "t5" in model_id.lower():
                # Text-to-text model
                pipe = pipeline("text2text-generation", model=model_id, device="cpu")
            else:
                # Default to text generation
                pipe = pipeline("text-generation", model=model_id, device="cpu")
            
            self.local_models[model_id] = pipe
            logger.info(f"Model loaded successfully: {model_id}")
            return pipe
            
        except Exception as e:
            logger.error(f"Error loading model {model_id}: {e}")
            return None
    
    def handle_inference(self):
        """Handle model inference requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            model_id = request_data.get('model_id')
            inputs = request_data.get('inputs')
            use_local = request_data.get('use_local', False)  # New parameter
            
            if not model_id or not inputs:
                self.send_error(400, "Missing model_id or inputs")
                return
            
            result = None
            
            # Try local inference first if requested and available
            if use_local and TRANSFORMERS_AVAILABLE:
                pipe = self.load_local_model(model_id)
                if pipe:
                    try:
                        logger.info(f"Running local inference for {model_id}")
                        result = pipe(inputs)
                        logger.info("Local inference completed")
                    except Exception as e:
                        logger.error(f"Local inference failed: {e}")
                        result = None
            
            # Fallback to API if local inference failed or not requested
            if result is None:
                logger.info(f"Using API inference for {model_id}")
                headers = {}
                if self.hf_token:
                    headers["Authorization"] = f"Bearer {self.hf_token}"
                
                url = f"{self.api_url}/models/{model_id}"
                payload = {"inputs": inputs}
                
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                else:
                    self.send_error(response.status_code, f"Inference failed: {response.text}")
                    return
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"result": result, "method": "local" if use_local and TRANSFORMERS_AVAILABLE else "api"}).encode())
                
        except Exception as e:
            logger.error(f"Error handling inference: {e}")
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info(f"{self.address_string()} - {format % args}")

def load_config():
    """Load configuration from JSON file"""
    try:
        with open('mcp_server_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Config file not found, using defaults")
        return {
            "api": {"base_url": "https://api-inference.huggingface.co"},
            "logging": {"level": "INFO"}
        }

def start_server(port=3000):
    """Start the MCP server"""
    config = load_config()
    
    # Set up logging level from config
    log_level = getattr(logging, config.get('logging', {}).get('level', 'INFO'))
    logging.getLogger().setLevel(log_level)
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, MCPHandler)
    
    logger.info(f"Starting MCP server on port {port}")
    logger.info(f"Health check: http://localhost:{port}/health")
    logger.info(f"Models endpoint: http://localhost:{port}/models")
    logger.info(f"Inference endpoint: http://localhost:{port}/inference")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        httpd.shutdown()

if __name__ == "__main__":
    port = int(os.getenv("MCP_SERVER_PORT", 3000))
    start_server(port) 
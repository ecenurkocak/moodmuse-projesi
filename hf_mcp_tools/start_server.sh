#!/bin/bash

echo "Starting Hugging Face MCP Server..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

# Check if requirements are installed
echo "Checking requirements..."
if ! python3 -c "import requests" &> /dev/null; then
    echo "Installing requirements..."
    pip3 install -r requirements.txt
fi

# Check if transformers is installed
if ! python3 -c "import transformers" &> /dev/null; then
    echo "Installing transformers and torch..."
    pip3 install transformers torch accelerate sentencepiece protobuf
fi

# Set environment variables (optional)
if [ -z "$HF_TOKEN" ]; then
    echo "Warning: HF_TOKEN not set. Some models may not work."
    echo "To set token: export HF_TOKEN=your_token_here"
fi

# Start the server
echo "Starting server on port 3000..."
echo "Press Ctrl+C to stop the server"
echo
python3 hf_mcp_server.py 
#!/bin/bash

echo "Testing Hugging Face MCP Server..."
echo

# Check if server is running
echo "Checking if server is running..."
if ! curl -s http://localhost:3000/health > /dev/null 2>&1; then
    echo "Error: Server is not running. Please start the server first."
    echo "Run: ./start_server.sh"
    exit 1
fi

# Run tests
echo "Running tests..."
python3 test_mcp_client.py 
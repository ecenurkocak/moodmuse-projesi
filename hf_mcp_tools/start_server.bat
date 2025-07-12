@echo off
echo Starting Hugging Face MCP Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking requirements...
pip show requests >nul 2>&1
if errorlevel 1 (
    echo Installing requirements...
    pip install -r requirements.txt
)

REM Check if transformers is installed
pip show transformers >nul 2>&1
if errorlevel 1 (
    echo Installing transformers and torch...
    pip install transformers torch accelerate sentencepiece protobuf
)

REM Set environment variables (optional)
if not defined HF_TOKEN (
    echo Warning: HF_TOKEN not set. Some models may not work.
    echo To set token: set HF_TOKEN=your_token_here
)

REM Start the server
echo Starting server on port 3000...
echo Press Ctrl+C to stop the server
echo.
python hf_mcp_server.py

pause 
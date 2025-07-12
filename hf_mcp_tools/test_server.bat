@echo off
echo Testing Hugging Face MCP Server...
echo.

REM Check if server is running
echo Checking if server is running...
curl -s http://localhost:3000/health >nul 2>&1
if errorlevel 1 (
    echo Error: Server is not running. Please start the server first.
    echo Run: start_server.bat
    pause
    exit /b 1
)

REM Run tests
echo Running tests...
python test_mcp_client.py

pause 
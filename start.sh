#!/bin/bash

# YouTube Content Analyzer - Launch Script
# Starts both backend and frontend servers

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
print_colored() {
    echo -e "${1}${2}${NC}"
}

# Function to check if port is in use
check_port() {
    lsof -i :$1 &>/dev/null
    return $?
}

# Function to kill process on port
kill_port() {
    if check_port $1; then
        print_colored $YELLOW "Port $1 is in use. Stopping existing process..."
        lsof -ti:$1 | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
}

print_colored $PURPLE "
╔══════════════════════════════════════════════╗
║     YouTube Content Analyzer                ║
║     Powered by yt-dlp & AI Analysis        ║
╚══════════════════════════════════════════════╝
"

# Check and install backend dependencies
print_colored $BLUE "\n📦 Checking backend dependencies..."
cd backend

if [ ! -d "venv" ]; then
    print_colored $YELLOW "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
print_colored $YELLOW "Installing Python packages..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Download spacy model if not present
python -m spacy download en_core_web_sm 2>/dev/null || true

# Check and install frontend dependencies
print_colored $BLUE "\n📦 Checking frontend dependencies..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    print_colored $YELLOW "Installing frontend dependencies..."
    npm install
fi

# Kill existing processes on our ports
kill_port 8012
kill_port 3025

# Start backend server
print_colored $GREEN "\n🚀 Starting backend server on port 8012..."
cd ../backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!

# Wait for backend to start
print_colored $YELLOW "Waiting for backend to initialize..."
for i in {1..10}; do
    if curl -s http://localhost:8012 >/dev/null 2>&1; then
        print_colored $GREEN "✅ Backend is ready!"
        break
    fi
    sleep 1
done

# Start frontend server
print_colored $GREEN "\n🚀 Starting frontend server on port 3025..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to start
print_colored $YELLOW "Waiting for frontend to initialize..."
sleep 5

# Open browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:3025
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://localhost:3025
fi

print_colored $GREEN "\n✨ YouTube Content Analyzer is running!"
print_colored $BLUE "
📍 Frontend: http://localhost:3025
📍 Backend API: http://localhost:8012
📍 API Docs: http://localhost:8012/docs

Press Ctrl+C to stop all servers
"

# Function to cleanup on exit
cleanup() {
    print_colored $YELLOW "\n\nShutting down servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    print_colored $RED "Servers stopped. Goodbye! 👋"
    exit 0
}

# Set up trap to cleanup on Ctrl+C
trap cleanup INT

# Keep script running
wait $BACKEND_PID $FRONTEND_PID
#!/bin/bash

# LUXORANOVA Website - Quick Start Script
# This script helps you quickly deploy and test the website

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}LUXORANOVA Website - Quick Start${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to display menu
show_menu() {
    echo -e "${GREEN}Select an option:${NC}"
    echo "1) Start local development server (Python)"
    echo "2) Start local development server (Node.js)"
    echo "3) Build Docker image"
    echo "4) Run Docker container"
    echo "5) Deploy to Netlify"
    echo "6) Deploy to Vercel"
    echo "7) Validate HTML/CSS/JS"
    echo "8) Exit"
    echo ""
    read -p "Enter choice [1-8]: " choice
}

# Function to start Python server
start_python_server() {
    echo -e "${GREEN}Starting Python HTTP server on port 8080...${NC}"
    python3 -m http.server 8080
}

# Function to start Node.js server
start_node_server() {
    if ! command -v npx &> /dev/null; then
        echo -e "${RED}Node.js is not installed. Please install Node.js first.${NC}"
        return 1
    fi
    echo -e "${GREEN}Starting Node.js HTTP server on port 8080...${NC}"
    npx http-server -p 8080
}

# Function to build Docker image
build_docker() {
    echo -e "${GREEN}Building Docker image...${NC}"
    docker build -t luxoranova-website:latest .
    echo -e "${GREEN}Docker image built successfully!${NC}"
    echo -e "${YELLOW}Run with: docker run -d -p 80:80 luxoranova-website:latest${NC}"
}

# Function to run Docker container
run_docker() {
    echo -e "${GREEN}Running Docker container...${NC}"
    docker run -d -p 80:80 --name luxoranova-web luxoranova-website:latest
    echo -e "${GREEN}Container started successfully!${NC}"
    echo -e "${YELLOW}Access at: http://localhost${NC}"
    echo -e "${YELLOW}Stop with: docker stop luxoranova-web${NC}"
    echo -e "${YELLOW}Remove with: docker rm luxoranova-web${NC}"
}

# Function to deploy to Netlify
deploy_netlify() {
    if ! command -v netlify &> /dev/null; then
        echo -e "${YELLOW}Netlify CLI not found. Installing...${NC}"
        npm install -g netlify-cli
    fi
    echo -e "${GREEN}Deploying to Netlify...${NC}"
    netlify deploy --prod --dir .
}

# Function to deploy to Vercel
deploy_vercel() {
    if ! command -v vercel &> /dev/null; then
        echo -e "${YELLOW}Vercel CLI not found. Installing...${NC}"
        npm install -g vercel
    fi
    echo -e "${GREEN}Deploying to Vercel...${NC}"
    vercel --prod
}

# Function to validate files
validate_files() {
    echo -e "${GREEN}Validating files...${NC}"
    
    # Check if files exist
    if [ ! -f "index.html" ]; then
        echo -e "${RED}❌ index.html not found${NC}"
        return 1
    fi
    echo -e "${GREEN}✓ index.html found${NC}"
    
    if [ ! -f "css/style.css" ]; then
        echo -e "${RED}❌ css/style.css not found${NC}"
        return 1
    fi
    echo -e "${GREEN}✓ css/style.css found${NC}"
    
    if [ ! -f "js/main.js" ]; then
        echo -e "${RED}❌ js/main.js not found${NC}"
        return 1
    fi
    echo -e "${GREEN}✓ js/main.js found${NC}"
    
    # Validate JavaScript
    if command -v node &> /dev/null; then
        if node -c js/main.js 2>&1; then
            echo -e "${GREEN}✓ JavaScript syntax valid${NC}"
        else
            echo -e "${RED}❌ JavaScript syntax errors found${NC}"
            return 1
        fi
    fi
    
    echo -e "${GREEN}All validations passed!${NC}"
}

# Main loop
while true; do
    show_menu
    case $choice in
        1)
            start_python_server
            ;;
        2)
            start_node_server
            ;;
        3)
            build_docker
            ;;
        4)
            run_docker
            ;;
        5)
            deploy_netlify
            ;;
        6)
            deploy_vercel
            ;;
        7)
            validate_files
            ;;
        8)
            echo -e "${BLUE}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please try again.${NC}"
            ;;
    esac
    echo ""
    read -p "Press Enter to continue..."
    clear
done

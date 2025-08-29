#!/bin/bash

# Hospital Management System Setup Script

echo "🏥 Hospital Management System - Automated Setup"
echo "============================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Python dependencies
install_dependencies() {
    echo "📦 Installing Python dependencies..."
    if command_exists pip3; then
        pip3 install -r requirements.txt
    elif command_exists pip; then
        pip install -r requirements.txt
    else
        echo "❌ pip not found. Please install Python and pip first."
        exit 1
    fi
}

# Function to setup environment
setup_environment() {
    echo "⚙️  Setting up environment..."
    
    # Copy environment file if it doesn't exist
    if [ ! -f .env ]; then
        echo "📋 Creating .env file..."
        cp .env.example .env
        echo "✅ .env file created from template"
        echo "⚠️  Please edit .env file with your database credentials"
    else
        echo "ℹ️  .env file already exists"
    fi
    
    # Create necessary directories
    echo "📁 Creating directories..."
    mkdir -p logs uploads app/static/uploads
    echo "✅ Directories created"
}

# Function to initialize database
init_database() {
    echo "🗄️  Initializing database..."
    
    if command_exists python3; then
        python3 scripts/init_db.py
    elif command_exists python; then
        python scripts/init_db.py
    else
        echo "❌ Python not found. Please install Python first."
        exit 1
    fi
}

# Function to start the server
start_server() {
    echo "🚀 Starting Hospital Management System server..."
    
    if command_exists python3; then
        python3 start.py
    elif command_exists python; then
        python start.py
    else
        echo "❌ Python not found. Please install Python first."
        exit 1
    fi
}

# Main execution
main() {
    echo "Starting setup process..."
    
    # Check if we're in the correct directory
    if [ ! -f "requirements.txt" ]; then
        echo "❌ requirements.txt not found. Please run this script from the project root directory."
        exit 1
    fi
    
    # Setup steps
    setup_environment
    install_dependencies
    init_database
    
    echo ""
    echo "✅ Setup completed successfully!"
    echo ""
    echo "🔗 Access URLs:"
    echo "   Web Interface: http://localhost:8000"
    echo "   API Documentation: http://localhost:8000/docs"
    echo ""
    echo "🔐 Default Login:"
    echo "   Username: admin"
    echo "   Password: admin123"
    echo ""
    
    # Ask if user wants to start the server
    read -p "Do you want to start the server now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start_server
    else
        echo "You can start the server later by running: python start.py"
    fi
}

# Run main function
main "$@"
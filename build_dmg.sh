#!/bin/bash

# Hospital Management System - DMG Builder
# This script specifically builds the macOS DMG file

echo "🏥 Hospital Management System - DMG Builder"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the desktop directory
if [ ! -f "package.json" ]; then
    print_error "package.json not found. Please run this script from the desktop directory."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node >/dev/null 2>&1; then
    print_error "Node.js is not installed. Please install Node.js first."
    echo "Download from: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm >/dev/null 2>&1; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi

echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"
echo ""

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        print_error "Failed to install dependencies."
        exit 1
    fi
    print_success "Dependencies installed successfully"
else
    echo "Dependencies already installed"
fi

# Check if required assets exist
echo "Checking build assets..."

required_files=("assets/icon.icns" "assets/dmg-background.png" "build/entitlements.mac.plist")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    print_warning "Some required files are missing:"
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "Creating placeholder files..."
    
    # Create placeholder icon if missing
    if [ ! -f "assets/icon.icns" ]; then
        echo "# Placeholder macOS icon" > assets/icon.icns
    fi
    
    # Create placeholder background if missing
    if [ ! -f "assets/dmg-background.png" ]; then
        echo "# Placeholder DMG background" > assets/dmg-background.png
    fi
fi

print_success "Build assets ready"

# Clean previous builds if requested
echo "Cleaning previous builds..."
if [ -d "dist" ]; then
    rm -rf dist/
    echo "Previous builds cleaned"
fi

# Build the DMG
echo ""
echo "Building macOS DMG file..."
echo "This may take several minutes..."

npm run build:mac

if [ $? -eq 0 ]; then
    print_success "DMG build completed successfully!"
    
    # Show results
    if [ -d "dist" ]; then
        echo ""
        echo "📦 Built files:"
        find dist/ -name "*.dmg" | while read file; do
            size=$(du -h "$file" | cut -f1)
            echo "  🍎 $file ($size)"
        done
        
        echo ""
        echo "📍 Files location: $(pwd)/dist/"
        
        # Check file details
        dmg_files=$(find dist/ -name "*.dmg" | wc -l)
        if [ $dmg_files -eq 0 ]; then
            print_warning "No DMG files found in dist directory"
        else
            print_success "Found $dmg_files DMG file(s)"
        fi
    else
        print_warning "dist directory not found"
    fi
    
    echo ""
    echo "🎉 DMG creation completed!"
    echo ""
    echo "📋 Next steps:"
    echo "  1. Test the DMG file on macOS"
    echo "  2. Replace placeholder icons with real icons if needed"
    echo "  3. Configure code signing for distribution (optional)"
    echo ""
    echo "💡 Installation: Double-click the DMG file and drag the app to Applications folder"
    
else
    print_error "DMG build failed!"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "  1. Check Node.js and npm versions"
    echo "  2. Ensure all dependencies are installed"
    echo "  3. Check build logs above for specific errors"
    echo "  4. Try running: npm install electron-builder --save-dev"
    exit 1
fi
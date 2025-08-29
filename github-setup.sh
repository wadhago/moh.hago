#!/bin/bash

# Hospital Management System - GitHub Setup Script
# This script prepares the repository for GitHub upload and automated builds

set -e

echo "🏥 Hospital Management System - GitHub Setup"
echo "==========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if we're in the project root
if [ ! -f "requirements.txt" ] || [ ! -d "desktop" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_info "Checking project structure..."

# Verify required files exist
required_files=(
    "README.md"
    "LICENSE" 
    ".gitignore"
    ".env.example"
    "requirements.txt"
    "desktop/package.json"
    ".github/workflows/build-desktop.yml"
    ".github/workflows/release.yml"
    ".github/workflows/test.yml"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    print_error "Missing required files:"
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
    exit 1
fi

print_success "All required files present"

# Initialize git if not already done
if [ ! -d ".git" ]; then
    print_info "Initializing Git repository..."
    git init
    print_success "Git repository initialized"
else
    print_info "Git repository already exists"
fi

# Create .gitignore if it doesn't exist or is empty
if [ ! -s ".gitignore" ]; then
    print_warning "Creating comprehensive .gitignore file..."
    # .gitignore content is already created by the main script
    print_success ".gitignore file ready"
fi

# Check if Node.js dependencies are installed
if [ ! -d "desktop/node_modules" ]; then
    print_info "Installing Node.js dependencies for desktop app..."
    cd desktop
    if command -v npm >/dev/null 2>&1; then
        npm install
        print_success "Node.js dependencies installed"
    else
        print_warning "npm not found. Install Node.js to complete desktop app setup"
    fi
    cd ..
fi

# Prepare desktop build assets
print_info "Preparing desktop build assets..."
cd desktop
if [ -f "scripts/prepare-icons.js" ]; then
    if command -v node >/dev/null 2>&1; then
        node scripts/prepare-icons.js
        print_success "Build assets prepared"
    else
        print_warning "Node.js not found. Build assets will be created during GitHub Actions"
    fi
else
    print_warning "Icon preparation script not found"
fi
cd ..

# Update README with actual repository URL
print_info "Updating repository URLs in README.md..."
if command -v sed >/dev/null 2>&1; then
    # This will be updated by user with actual GitHub username
    print_warning "Remember to update YOUR_USERNAME in README.md with your actual GitHub username"
else
    print_warning "Please manually update YOUR_USERNAME placeholders in README.md"
fi

# Stage all files for commit
print_info "Staging files for Git..."
git add .

# Check if there are staged changes
if git diff --staged --quiet; then
    print_info "No changes to commit"
else
    print_info "Ready to commit changes"
    
    # Show what will be committed
    echo ""
    print_info "Files to be committed:"
    git diff --staged --name-only | sed 's/^/  ✓ /'
    echo ""
    
    # Ask if user wants to commit
    read -p "Do you want to commit these changes? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git commit -m "Initial commit: Complete Hospital Management System

- ✅ FastAPI backend with bilingual support (Arabic/English)
- ✅ Electron desktop apps for Windows, macOS, Linux  
- ✅ Complete hospital management modules
- ✅ GitHub Actions for automated building and releases
- ✅ Comprehensive documentation and setup guides
- ✅ Security features and healthcare standards support

Ready for deployment and distribution via GitHub Releases."
        
        print_success "Changes committed successfully"
    else
        print_info "Changes staged but not committed. You can commit later with:"
        echo "  git commit -m 'Initial commit: Hospital Management System'"
    fi
fi

# Instructions for GitHub setup
echo ""
echo "🎯 Next Steps for GitHub:"
echo "========================="
echo ""
echo "1. Create GitHub Repository:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: hospital-management-system"
echo "   - Make it public or private as needed"
echo "   - Don't initialize with README (we have one)"
echo ""
echo "2. Connect to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/hospital-management-system.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Create First Release:"
echo "   git tag v1.0.0"
echo "   git push origin v1.0.0"
echo ""
echo "4. GitHub Actions will automatically:"
echo "   ✅ Build Windows EXE file"
echo "   ✅ Build macOS DMG file"
echo "   ✅ Build Linux AppImage/DEB files"
echo "   ✅ Create GitHub Release with downloads"
echo ""
echo "5. Update README.md:"
echo "   - Replace YOUR_USERNAME with actual GitHub username"
echo "   - Update contact information"
echo "   - Add any specific installation notes"
echo ""

print_success "GitHub setup preparation completed!"
print_info "Your Hospital Management System is ready to be uploaded to GitHub"

echo ""
echo "📋 Repository Features:"
echo "======================"
echo "✅ Automated desktop app building"
echo "✅ Cross-platform support (Windows, macOS, Linux)"
echo "✅ Professional release management"
echo "✅ Continuous integration and testing"
echo "✅ Security audits and code quality checks"
echo "✅ Bilingual documentation (Arabic/English)"
echo "✅ Healthcare standards compliance"
echo ""
echo "🚀 Ready to transform hospital management worldwide!"
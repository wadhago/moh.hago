#!/bin/bash

# Hospital Management System Desktop Build Script
# Builds the application for multiple platforms

set -e

echo "🏥 Hospital Management System - Desktop Build Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check requirements
print_status "Checking build requirements..."

if ! command_exists npm; then
    print_error "npm is not installed. Please install Node.js and npm first."
    exit 1
fi

if ! command_exists python3 && ! command_exists python; then
    print_warning "Python not found in PATH. Desktop app will require Python to be installed on target machines."
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    print_status "Installing Node.js dependencies..."
    npm install
    print_success "Dependencies installed"
else
    print_status "Node.js dependencies already installed"
fi

# Create placeholder icons if they don't exist
print_status "Setting up build assets..."

create_placeholder_icon() {
    local size=$1
    local output=$2
    local format=$3
    
    if [ ! -f "$output" ]; then
        print_status "Creating placeholder icon: $output"
        
        # Create a simple SVG icon
        cat > temp_icon.svg << EOF
<svg width="$size" height="$size" xmlns="http://www.w3.org/2000/svg">
  <rect width="$size" height="$size" fill="#2563eb"/>
  <rect x="$((size/4))" y="$((size/8))" width="$((size/2))" height="$((size*3/8))" fill="white"/>
  <rect x="$((size/8))" y="$((size/4))" width="$((size*3/4))" height="$((size/2))" fill="white"/>
  <text x="50%" y="85%" font-family="Arial" font-size="$((size/8))" fill="white" text-anchor="middle">HMS</text>
</svg>
EOF
        
        # Convert to PNG using available tools
        if command_exists convert; then
            convert temp_icon.svg -resize ${size}x${size} "$output"
        elif command_exists rsvg-convert; then
            rsvg-convert -w $size -h $size temp_icon.svg -o "$output"
        else
            # Create a simple bitmap fallback
            print_warning "No SVG converter found. Creating simple PNG placeholder."
            # This would need ImageMagick or similar
        fi
        
        rm -f temp_icon.svg
    fi
}

# Create asset directories
mkdir -p assets
mkdir -p build

# Create basic icons
create_placeholder_icon 512 "assets/icon.png" "png"

# Copy icon for different formats (placeholder - should be replaced with proper conversions)
if [ ! -f "assets/icon.ico" ]; then
    print_status "Creating Windows icon..."
    cp assets/icon.png assets/icon.ico 2>/dev/null || true
fi

if [ ! -f "assets/icon.icns" ]; then
    print_status "Creating macOS icon..."
    cp assets/icon.png assets/icon.icns 2>/dev/null || true
fi

print_success "Build assets prepared"

# Build function
build_platform() {
    local platform=$1
    local description=$2
    
    print_status "Building for $description..."
    
    case $platform in
        "win")
            npm run build:win
            ;;
        "mac")
            npm run build:mac
            ;;
        "linux")
            npm run build:linux
            ;;
        "all")
            npm run build:all
            ;;
        *)
            print_error "Unknown platform: $platform"
            return 1
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        print_success "$description build completed"
        return 0
    else
        print_error "$description build failed"
        return 1
    fi
}

# Parse command line arguments
PLATFORM="all"
CLEAN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--platform)
            PLATFORM="$2"
            shift 2
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  -p, --platform PLATFORM    Build for specific platform (win|mac|linux|all)"
            echo "  -c, --clean                 Clean dist directory before building"
            echo "  -h, --help                  Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Clean dist directory if requested
if [ "$CLEAN" = true ]; then
    print_status "Cleaning dist directory..."
    rm -rf dist/
    print_success "Dist directory cleaned"
fi

# Build for specified platform(s)
print_status "Starting build process for platform: $PLATFORM"

case $PLATFORM in
    "win")
        build_platform "win" "Windows (EXE)"
        ;;
    "mac")
        build_platform "mac" "macOS (DMG)"
        ;;
    "linux")
        build_platform "linux" "Linux (AppImage/DEB)"
        ;;
    "all")
        print_status "Building for all platforms..."
        success_count=0
        total_count=3
        
        if build_platform "win" "Windows (EXE)"; then
            ((success_count++))
        fi
        
        if build_platform "mac" "macOS (DMG)"; then
            ((success_count++))
        fi
        
        if build_platform "linux" "Linux (AppImage/DEB)"; then
            ((success_count++))
        fi
        
        print_status "Build summary: $success_count/$total_count platforms built successfully"
        ;;
    *)
        print_error "Invalid platform: $PLATFORM"
        print_error "Valid platforms: win, mac, linux, all"
        exit 1
        ;;
esac

# Show results
if [ -d "dist" ]; then
    print_success "Build completed! Output files:"
    echo ""
    find dist/ -type f -name "*.exe" -o -name "*.dmg" -o -name "*.AppImage" -o -name "*.deb" | while read file; do
        size=$(du -h "$file" | cut -f1)
        echo "  📦 $file ($size)"
    done
    echo ""
    print_status "Total build size: $(du -sh dist/ | cut -f1)"
else
    print_error "No output directory found. Build may have failed."
    exit 1
fi

print_success "🎉 Desktop application build process completed!"
echo ""
echo "📋 Next steps:"
echo "  1. Test the built applications on target platforms"
echo "  2. Replace placeholder icons with your hospital's branding"
echo "  3. Configure code signing for production distribution"
echo "  4. Set up automatic updates (optional)"
echo ""
echo "💡 Tip: Use './build.sh -p win' to build only Windows version"
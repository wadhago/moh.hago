#!/bin/bash

# Icon Creation Script for Hospital Management System

echo "🎨 Creating icons for Hospital Management System..."

cd "$(dirname "$0")"

# Create assets directory if it doesn't exist
mkdir -p assets

# Create a simple SVG icon for the hospital system
cat > assets/icon.svg << 'EOF'
<svg width="512" height="512" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#2563eb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1d4ed8;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="2" dy="2" stdDeviation="4" flood-opacity="0.3"/>
    </filter>
  </defs>
  
  <!-- Background circle -->
  <circle cx="256" cy="256" r="240" fill="url(#bg)" filter="url(#shadow)"/>
  
  <!-- Cross symbol -->
  <rect x="226" y="156" width="60" height="200" rx="10" fill="white"/>
  <rect x="156" y="226" width="200" height="60" rx="10" fill="white"/>
  
  <!-- Medical symbol accents -->
  <circle cx="256" cy="256" r="85" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="3"/>
  <circle cx="256" cy="256" r="110" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  
  <!-- Hospital text -->
  <text x="256" y="420" font-family="Arial, sans-serif" font-size="42" font-weight="bold" 
        text-anchor="middle" fill="white">HMS</text>
</svg>
EOF

echo "✅ Created SVG icon"

# Function to convert SVG to PNG using available tools
convert_svg_to_png() {
    local size=$1
    local output=$2
    
    if command -v convert >/dev/null 2>&1; then
        # Using ImageMagick
        echo "🔄 Converting SVG to PNG ($size x $size) using ImageMagick..."
        convert assets/icon.svg -resize ${size}x${size} "$output"
    elif command -v rsvg-convert >/dev/null 2>&1; then
        # Using librsvg
        echo "🔄 Converting SVG to PNG ($size x $size) using rsvg-convert..."
        rsvg-convert -w $size -h $size assets/icon.svg -o "$output"
    elif command -v inkscape >/dev/null 2>&1; then
        # Using Inkscape
        echo "🔄 Converting SVG to PNG ($size x $size) using Inkscape..."
        inkscape assets/icon.svg --export-filename="$output" --export-width=$size --export-height=$size
    else
        echo "❌ No SVG converter found. Please install ImageMagick, librsvg, or Inkscape"
        return 1
    fi
}

# Create PNG icons
convert_svg_to_png 512 "assets/icon.png"
convert_svg_to_png 256 "assets/icon-256.png"
convert_svg_to_png 128 "assets/icon-128.png"
convert_svg_to_png 64 "assets/icon-64.png"
convert_svg_to_png 32 "assets/icon-32.png"
convert_svg_to_png 16 "assets/icon-16.png"

# Create macOS icon set (icns)
if command -v iconutil >/dev/null 2>&1; then
    echo "🍎 Creating macOS icon set..."
    
    # Create iconset directory
    mkdir -p assets/icon.iconset
    
    # Copy PNG files to iconset with proper naming
    cp assets/icon-16.png assets/icon.iconset/icon_16x16.png
    cp assets/icon-32.png assets/icon.iconset/icon_16x16@2x.png
    cp assets/icon-32.png assets/icon.iconset/icon_32x32.png
    cp assets/icon-64.png assets/icon.iconset/icon_32x32@2x.png
    cp assets/icon-128.png assets/icon.iconset/icon_128x128.png
    cp assets/icon-256.png assets/icon.iconset/icon_128x128@2x.png
    cp assets/icon-256.png assets/icon.iconset/icon_256x256.png
    cp assets/icon.png assets/icon.iconset/icon_256x256@2x.png
    cp assets/icon.png assets/icon.iconset/icon_512x512.png
    
    # Create icns file
    iconutil -c icns assets/icon.iconset -o assets/icon.icns
    
    # Clean up
    rm -rf assets/icon.iconset
    
    echo "✅ Created icon.icns"
else
    echo "⚠️  iconutil not found. Copying PNG as placeholder for icns..."
    cp assets/icon.png assets/icon.icns
fi

# Create Windows icon (ico)
if command -v convert >/dev/null 2>&1; then
    echo "🪟 Creating Windows icon..."
    convert assets/icon-16.png assets/icon-32.png assets/icon-64.png assets/icon-128.png assets/icon-256.png assets/icon.ico
    echo "✅ Created icon.ico"
else
    echo "⚠️  ImageMagick not found. Copying PNG as placeholder for ico..."
    cp assets/icon.png assets/icon.ico
fi

# Create DMG background
echo "🖼️ Creating DMG background..."
cat > assets/dmg-background.svg << 'EOF'
<svg width="540" height="380" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f8fafc;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#e2e8f0;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <rect width="540" height="380" fill="url(#bgGradient)"/>
  
  <!-- Header -->
  <rect x="0" y="0" width="540" height="80" fill="#2563eb" opacity="0.1"/>
  <text x="270" y="35" font-family="Arial, sans-serif" font-size="24" font-weight="bold" 
        text-anchor="middle" fill="#1e40af">Hospital Management System</text>
  <text x="270" y="55" font-family="Arial, sans-serif" font-size="14" 
        text-anchor="middle" fill="#64748b">Drag the application to your Applications folder</text>
  
  <!-- Decorative elements -->
  <circle cx="100" cy="300" r="40" fill="#2563eb" opacity="0.05"/>
  <circle cx="440" cy="300" r="30" fill="#10b981" opacity="0.05"/>
  
  <!-- Instructions -->
  <text x="270" y="320" font-family="Arial, sans-serif" font-size="12" 
        text-anchor="middle" fill="#64748b">Install by dragging to Applications →</text>
</svg>
EOF

# Convert DMG background to PNG
convert_svg_to_png 540 "assets/dmg-background.png"

echo "✅ Created DMG background"

echo ""
echo "🎉 Icon creation completed!"
echo "Created files:"
echo "  📱 icon.png (512x512)"
echo "  🍎 icon.icns (macOS)"
echo "  🪟 icon.ico (Windows)"
echo "  🖼️ dmg-background.png"
echo ""
echo "Next: Run 'npm run build:mac' to create the DMG file"
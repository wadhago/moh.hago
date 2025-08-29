# Hospital Management System - Icon Assets

This directory contains icon files for different platforms:

## Icon Files

- `icon.png` - 512x512 PNG for Linux and general use
- `icon.ico` - Windows ICO format (contains multiple sizes: 16, 32, 48, 64, 128, 256)
- `icon.icns` - macOS ICNS format (contains multiple sizes for Retina displays)

## DMG Background

- `dmg-background.png` - Background image for macOS DMG installer

## Icon Creation

To create proper icons from a source image:

### From PNG to ICO (Windows)
```bash
# Using ImageMagick
convert icon.png -define icon:auto-resize=16,32,48,64,128,256 icon.ico

# Or using online converter
# Upload to https://www.icoconverter.com/
```

### From PNG to ICNS (macOS)
```bash
# Create iconset directory
mkdir icon.iconset

# Generate different sizes
sips -z 16 16 icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32 icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32 icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64 icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128 icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256 icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256 icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512 icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512 icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png

# Create ICNS file
iconutil -c icns icon.iconset
```

## Current Icons

The current icon is a medical cross symbol representing the Hospital Management System. 

To replace with your hospital's logo:
1. Create a 1024x1024 PNG with your logo
2. Follow the conversion steps above
3. Replace the existing icon files

## Note

Placeholder icon files have been created for the build system to work. Replace these with actual hospital branding icons for production use.
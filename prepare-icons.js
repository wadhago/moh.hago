const fs = require('fs');
const path = require('path');

/**
 * Prepare Icons Script for Hospital Management System
 * Creates placeholder icons if they don't exist for GitHub Actions builds
 */

console.log('🎨 Preparing icons for Hospital Management System...');

const assetsDir = path.join(__dirname, '..', 'assets');
const buildDir = path.join(__dirname, '..', 'build');

// Ensure directories exist
if (!fs.existsSync(assetsDir)) {
    fs.mkdirSync(assetsDir, { recursive: true });
    console.log('✅ Created assets directory');
}

if (!fs.existsSync(buildDir)) {
    fs.mkdirSync(buildDir, { recursive: true });
    console.log('✅ Created build directory');
}

// Create SVG icon template
const svgIcon = `<svg width="512" height="512" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#2563eb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1d4ed8;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <circle cx="256" cy="256" r="240" fill="url(#bg)"/>
  
  <!-- Medical Cross -->
  <rect x="216" y="146" width="80" height="220" rx="15" fill="white"/>
  <rect x="146" y="216" width="220" height="80" rx="15" fill="white"/>
  
  <!-- HMS Text -->
  <text x="256" y="400" font-family="Arial, sans-serif" font-size="48" font-weight="bold" 
        text-anchor="middle" fill="white">HMS</text>
</svg>`;

// Create DMG background SVG
const dmgBackground = `<svg width="540" height="380" xmlns="http://www.w3.org/2000/svg">
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
        text-anchor="middle" fill="#64748b">نظام إدارة المستشفيات</text>
  
  <!-- Installation instruction -->
  <text x="270" y="320" font-family="Arial, sans-serif" font-size="16" 
        text-anchor="middle" fill="#374151">Drag application to Applications folder</text>
  <text x="270" y="340" font-family="Arial, sans-serif" font-size="14" 
        text-anchor="middle" fill="#6b7280">اسحب التطبيق إلى مجلد التطبيقات</text>
</svg>`;

// Function to create placeholder files
function createPlaceholderFile(filePath, content, description) {
    if (!fs.existsSync(filePath)) {
        fs.writeFileSync(filePath, content);
        console.log(`✅ Created ${description}: ${path.basename(filePath)}`);
        return true;
    } else {
        console.log(`ℹ️  ${description} already exists: ${path.basename(filePath)}`);
        return false;
    }
}

// Define required files
const requiredFiles = [{
        path: path.join(assetsDir, 'icon.svg'),
        content: svgIcon,
        description: 'SVG icon'
    },
    {
        path: path.join(assetsDir, 'icon.png'),
        content: '# PNG icon placeholder - replace with actual PNG icon',
        description: 'PNG icon placeholder'
    },
    {
        path: path.join(assetsDir, 'icon.ico'),
        content: '# ICO icon placeholder - replace with actual ICO icon',
        description: 'ICO icon placeholder'
    },
    {
        path: path.join(assetsDir, 'icon.icns'),
        content: '# ICNS icon placeholder - replace with actual ICNS icon',
        description: 'ICNS icon placeholder'
    },
    {
        path: path.join(assetsDir, 'dmg-background.svg'),
        content: dmgBackground,
        description: 'DMG background SVG'
    },
    {
        path: path.join(assetsDir, 'dmg-background.png'),
        content: '# DMG background placeholder - replace with actual PNG background',
        description: 'DMG background placeholder'
    }
];

// Create macOS entitlements if not exists
const entitlementsPath = path.join(buildDir, 'entitlements.mac.plist');
const entitlementsContent = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.debugger</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
  </dict>
</plist>`;

requiredFiles.push({
    path: entitlementsPath,
    content: entitlementsContent,
    description: 'macOS entitlements'
});

// Create all required files
let createdCount = 0;
requiredFiles.forEach(file => {
    if (createPlaceholderFile(file.path, file.content, file.description)) {
        createdCount++;
    }
});

console.log(`\n🎉 Icon preparation completed!`);
console.log(`📁 Created ${createdCount} new files`);
console.log(`📋 Total files ready: ${requiredFiles.length}`);

if (createdCount > 0) {
    console.log(`\n⚠️  Note: Some placeholder files were created.`);
    console.log(`   For production builds, replace placeholders with actual icons:`);
    console.log(`   • Use PNG/ICO/ICNS converters for proper icon formats`);
    console.log(`   • Create proper DMG background image (540x380px)`);
    console.log(`   • Test icons on actual target platforms`);
}

console.log(`\n✅ Ready for electron-builder!`);

// Verify all files exist
const missingFiles = requiredFiles.filter(file => !fs.existsSync(file.path));
if (missingFiles.length === 0) {
    console.log(`✅ All required build assets are present`);
    process.exit(0);
} else {
    console.error(`❌ Missing files:`);
    missingFiles.forEach(file => {
        console.error(`   • ${path.basename(file.path)}`);
    });
    process.exit(1);
}
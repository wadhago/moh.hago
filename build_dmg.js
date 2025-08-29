const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🏥 Hospital Management System - DMG Builder');
console.log('==========================================');

// Function to execute command and handle errors
function executeCommand(command, description) {
    console.log(`\n📋 ${description}...`);
    try {
        const output = execSync(command, {
            stdio: 'inherit',
            cwd: __dirname
        });
        console.log(`✅ ${description} completed successfully`);
        return true;
    } catch (error) {
        console.error(`❌ ${description} failed:`, error.message);
        return false;
    }
}

// Check if required files exist
function checkRequiredFiles() {
    const requiredFiles = [
        'package.json',
        'src/main.js',
        'assets/icon.icns',
        'build/entitlements.mac.plist'
    ];

    console.log('\n🔍 Checking required files...');

    for (const file of requiredFiles) {
        if (!fs.existsSync(path.join(__dirname, file))) {
            console.log(`⚠️  Missing: ${file}`);

            // Create placeholder files if missing
            if (file === 'assets/icon.icns') {
                fs.writeFileSync(path.join(__dirname, file), '# Placeholder macOS icon');
                console.log(`📝 Created placeholder: ${file}`);
            }
        } else {
            console.log(`✅ Found: ${file}`);
        }
    }
}

// Main build process
async function buildDMG() {
    try {
        // Check Node.js and npm versions
        console.log('\n🔧 Environment Information:');
        console.log(`Node.js: ${process.version}`);

        try {
            const npmVersion = execSync('npm --version', { encoding: 'utf8' }).trim();
            console.log(`npm: ${npmVersion}`);
        } catch (error) {
            console.error('❌ npm not found');
            process.exit(1);
        }

        // Check required files
        checkRequiredFiles();

        // Install dependencies
        if (!fs.existsSync(path.join(__dirname, 'node_modules'))) {
            if (!executeCommand('npm install', 'Installing dependencies')) {
                process.exit(1);
            }
        } else {
            console.log('\n✅ Dependencies already installed');
        }

        // Clean previous builds
        const distDir = path.join(__dirname, 'dist');
        if (fs.existsSync(distDir)) {
            console.log('\n🧹 Cleaning previous builds...');
            fs.rmSync(distDir, { recursive: true, force: true });
            console.log('✅ Previous builds cleaned');
        }

        // Build DMG for macOS
        console.log('\n🍎 Building macOS DMG...');
        console.log('This may take several minutes...');

        if (!executeCommand('npm run build:mac', 'Building DMG')) {
            console.error('\n❌ DMG build failed!');
            console.log('\n🔧 Troubleshooting suggestions:');
            console.log('  1. Ensure you are running this on macOS');
            console.log('  2. Check that electron-builder is installed');
            console.log('  3. Try: npm install electron-builder --save-dev');
            console.log('  4. Check the error messages above');
            process.exit(1);
        }

        // Show results
        console.log('\n🎉 DMG build completed successfully!');

        if (fs.existsSync(distDir)) {
            console.log('\n📦 Built files:');

            const files = fs.readdirSync(distDir);
            const dmgFiles = files.filter(file => file.endsWith('.dmg'));

            if (dmgFiles.length > 0) {
                dmgFiles.forEach(file => {
                    const filePath = path.join(distDir, file);
                    const stats = fs.statSync(filePath);
                    const size = (stats.size / 1024 / 1024).toFixed(1) + ' MB';
                    console.log(`  🍎 ${file} (${size})`);
                });

                console.log(`\n📍 Files location: ${distDir}`);
                console.log(`\n✅ Successfully created ${dmgFiles.length} DMG file(s)`);
            } else {
                console.log('⚠️  No DMG files found in dist directory');
            }
        }

        console.log('\n📋 Next steps:');
        console.log('  1. Test the DMG file on macOS');
        console.log('  2. Double-click to mount the DMG');
        console.log('  3. Drag the app to Applications folder');
        console.log('  4. Run the app from Applications');
        console.log('\n💡 The DMG file is ready for distribution!');

    } catch (error) {
        console.error('\n❌ Build process failed:', error.message);
        process.exit(1);
    }
}

// Run the build process
buildDMG();
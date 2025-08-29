# Hospital Management System - Desktop Distribution Guide

## Overview

This guide covers building and distributing the Hospital Management System as desktop applications for Windows (.exe), macOS (.dmg), and as a Progressive Web App (PWA).

## 🖥️ Desktop Applications

### Prerequisites

1. **Node.js 16+**: Download from [nodejs.org](https://nodejs.org/)
2. **Python 3.8+**: Required for the backend server
3. **Platform-specific tools**:
   - **Windows**: No additional tools required
   - **macOS**: Xcode Command Line Tools (`xcode-select --install`)
   - **Linux**: Standard build tools (`build-essential`)

### Quick Build

Navigate to the desktop directory and run:

```bash
cd desktop

# Install dependencies
npm install

# Build for all platforms
npm run build:all

# Or build for specific platform
npm run build:win    # Windows EXE
npm run build:mac    # macOS DMG
npm run build:linux  # Linux AppImage/DEB
```

### Using Build Scripts

#### Linux/macOS
```bash
# Make executable
chmod +x build.sh

# Build all platforms
./build.sh

# Build specific platform
./build.sh --platform win
./build.sh --platform mac
./build.sh --platform linux

# Clean build
./build.sh --clean
```

#### Windows
```cmd
# Run Windows build script
build.bat
```

### Manual Build Process

1. **Prepare Environment**
   ```bash
   cd desktop
   npm install
   ```

2. **Create Icons** (Replace placeholders with your hospital's branding)
   - `assets/icon.png` (512×512 for Linux/general use)
   - `assets/icon.ico` (Windows, multiple sizes: 16,32,48,64,128,256)
   - `assets/icon.icns` (macOS, multiple resolutions including Retina)

3. **Configure package.json**
   - Update app name, version, and description
   - Modify build settings in the `"build"` section
   - Set up code signing certificates (for production)

4. **Build Applications**
   ```bash
   # Individual platform builds
   npx electron-builder --win
   npx electron-builder --mac  
   npx electron-builder --linux
   
   # All platforms at once
   npx electron-builder --win --mac --linux
   ```

### Output Files

After building, you'll find the following in the `dist/` directory:

#### Windows
- `Hospital Management System Setup.exe` - NSIS installer
- `Hospital Management System.exe` - Portable executable

#### macOS  
- `Hospital Management System-1.0.0.dmg` - DMG disk image
- `Hospital Management System-1.0.0-mac.zip` - ZIP archive

#### Linux
- `Hospital Management System-1.0.0.AppImage` - AppImage executable
- `hospital-management-system_1.0.0_amd64.deb` - Debian package

## 🌐 Progressive Web App (PWA)

### Features
- **Offline Functionality**: Core features work without internet
- **Install Prompt**: Can be installed from browser
- **App-like Experience**: Fullscreen, standalone window
- **Push Notifications**: Real-time alerts (future feature)
- **Background Sync**: Sync data when connection returns

### Installation

The PWA is automatically available when the web server is running. Users can:

1. **Chrome/Edge**: Click install button in address bar or "Add to Home Screen"
2. **Safari**: Share → Add to Home Screen
3. **Mobile**: "Add to Home Screen" from browser menu

### Configuration

PWA settings are in `/static/manifest.json`:
- App name and description
- Icons for different sizes
- Theme colors
- Shortcuts and screenshots

### Service Worker

The Service Worker (`/static/js/sw.js`) provides:
- **Caching Strategy**: Static files cached, API calls network-first
- **Offline Pages**: Custom offline experience
- **Background Sync**: Queue actions when offline
- **Push Notifications**: Future notification support

## 🚀 Deployment Options

### Option 1: Desktop Application Distribution

#### Windows
1. **Code Signing** (Recommended for production):
   ```json
   "win": {
     "certificateFile": "path/to/certificate.p12",
     "certificatePassword": "password"
   }
   ```

2. **Distribution**:
   - Upload to hospital website
   - Distribute via network share
   - Use Microsoft SCCM for enterprise deployment
   - Submit to Microsoft Store (optional)

#### macOS
1. **Code Signing** (Required for macOS 10.15+):
   ```json
   "mac": {
     "identity": "Developer ID Application: Your Name",
     "hardenedRuntime": true,
     "notarize": true
   }
   ```

2. **Notarization** (Required):
   ```bash
   # Set environment variables
   export APPLE_ID="your-apple-id@email.com"
   export APPLE_ID_PASSWORD="app-specific-password"
   
   # Build with notarization
   npm run build:mac
   ```

3. **Distribution**:
   - Direct download from website
   - Enterprise deployment via MDM
   - Submit to Mac App Store (optional)

#### Linux
1. **Distribution**:
   - AppImage for universal compatibility
   - DEB packages for Debian/Ubuntu
   - RPM packages for Red Hat/Fedora
   - Snap packages for Ubuntu
   - Flatpak for various distributions

### Option 2: Web Application Deployment

#### Traditional Web Hosting
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with production settings

# Initialize database
python scripts/init_db.py

# Start with production server
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### Docker Deployment
```bash
# Build image
docker build -t hospital-management-system .

# Run container
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e SECRET_KEY="production-secret" \
  hospital-management-system
```

#### Cloud Deployment
- **Heroku**: `git push heroku main`
- **Google Cloud Run**: Deploy container
- **AWS ECS**: Deploy with load balancer
- **Azure Container Instances**: Deploy container

## 🔧 Production Considerations

### Security
1. **Change Default Credentials**: Update admin password immediately
2. **Environment Variables**: Use production-grade secrets
3. **HTTPS**: Enable SSL/TLS encryption
4. **Database Security**: Use strong passwords and restricted access
5. **Code Signing**: Sign desktop applications

### Performance
1. **Database**: Use PostgreSQL for production
2. **Caching**: Enable Redis for better performance  
3. **CDN**: Serve static files from CDN
4. **Load Balancing**: Use multiple server instances
5. **Monitoring**: Implement health checks and logging

### Updates
1. **Auto Updates**: Configure electron-updater for desktop apps
2. **PWA Updates**: Service worker handles web app updates
3. **Database Migration**: Plan for schema changes
4. **Rollback Plan**: Prepare rollback procedures

## 📱 Mobile Considerations

### PWA on Mobile
- **iOS**: Installable from Safari, limited push notification support
- **Android**: Full PWA support including notifications
- **Installation**: Works like native app once installed

### Future Native Mobile Apps
The same FastAPI backend can serve:
- React Native mobile apps
- Flutter applications
- Ionic hybrid apps

## 🎯 Distribution Checklist

### Before Distribution
- [ ] Replace placeholder icons with hospital branding
- [ ] Update app name and version numbers
- [ ] Configure production database settings
- [ ] Test on target operating systems
- [ ] Set up code signing certificates
- [ ] Create user documentation
- [ ] Plan update distribution method

### Post-Distribution
- [ ] Monitor application performance
- [ ] Collect user feedback
- [ ] Plan regular updates
- [ ] Set up support channels
- [ ] Document deployment process
- [ ] Train hospital staff

## 📞 Support

For technical support:
1. Check application logs in desktop app menu
2. Review browser console for web app issues
3. Verify Python backend is running properly
4. Ensure database connectivity
5. Check firewall and network settings

---

**Hospital Management System Desktop Distribution Guide v1.0.0**  
*Complete healthcare solution for desktop and web*
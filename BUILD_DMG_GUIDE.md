# إنشاء ملف DMG لنظام إدارة المستشفيات
# Building DMG for Hospital Management System

## المتطلبات المطلوبة / Prerequisites

لإنشاء ملف DMG على نظام macOS، تحتاج إلى:
To create a DMG file on macOS, you need:

1. **Node.js** (إصدار 16 أو أحدث / version 16 or higher)
2. **npm** (يأتي مع Node.js / comes with Node.js)
3. **Python 3** (لتشغيل الخادم / for running the backend server)

## خطوات التثبيت / Installation Steps

### 1. تثبيت Node.js / Install Node.js

```bash
# تحميل وتثبيت Node.js من الموقع الرسمي
# Download and install Node.js from official website
# https://nodejs.org/

# أو استخدام Homebrew إذا كان متوفراً
# Or using Homebrew if available
brew install node
```

### 2. التحقق من التثبيت / Verify Installation

```bash
node --version
npm --version
```

### 3. تثبيت المكتبات المطلوبة / Install Dependencies

```bash
cd /Users/mohammedalmogadum/Desktop/MS/desktop
npm install
```

## إنشاء ملف DMG / Building DMG

### الطريقة الأولى: البناء التلقائي / Method 1: Automatic Build

```bash
cd /Users/mohammedalmogadum/Desktop/MS/desktop

# إنشاء ملف DMG فقط
# Build DMG only
npm run build:mac

# إنشاء جميع الصيغ (Windows, macOS, Linux)
# Build all formats
npm run build:all
```

### الطريقة الثانية: استخدام سكريبت البناء / Method 2: Using Build Script

```bash
cd /Users/mohammedalmogadum/Desktop/MS/desktop

# منح صلاحيات التنفيذ للسكريبت
# Grant execution permissions
chmod +x build.sh

# تشغيل السكريبت لإنشاء DMG
# Run script to build DMG
./build.sh --platform mac

# أو لإنشاء جميع الصيغ
# Or to build all formats
./build.sh --platform all
```

## مواقع الملفات المُنشأة / Output File Locations

بعد نجاح البناء، ستجد الملفات في:
After successful build, you'll find files in:

```
/Users/mohammedalmogadum/Desktop/MS/desktop/dist/
├── Hospital Management System-1.0.0.dmg          # ملف DMG للتثبيت
├── Hospital Management System-1.0.0-arm64.dmg    # للأجهزة بمعالج Apple Silicon
└── Hospital Management System-1.0.0-x64.dmg      # للأجهزة بمعالج Intel
```

## استكشاف الأخطاء / Troubleshooting

### خطأ: "node command not found"
```bash
# تثبيت Node.js من:
# Install Node.js from:
# https://nodejs.org/en/download/
```

### خطأ: "electron-builder not found"
```bash
cd /Users/mohammedalmogadum/Desktop/MS/desktop
npm install electron-builder --save-dev
```

### خطأ: "icon file not found"
```bash
# تأكد من وجود ملفات الرموز في مجلد assets
# Make sure icon files exist in assets folder
ls -la assets/
```

### خطأ في الرموز / Icon Issues
```bash
# إنشاء الرموز باستخدام السكريبت المُرفق
# Create icons using the provided script
chmod +x create_icons.sh
./create_icons.sh
```

## معلومات إضافية / Additional Information

### خصائص ملف DMG / DMG Features
- **التثبيت السهل**: سحب وإفلات إلى مجلد التطبيقات
- **Easy Installation**: Drag and drop to Applications folder
- **توقيع رقمي**: مُعد للتوقيع (يتطلب شهادة مطور)
- **Code Signing**: Ready for signing (requires developer certificate)
- **متوافق مع**: macOS 10.13 وأحدث
- **Compatible with**: macOS 10.13 and later

### أحجام الملفات المتوقعة / Expected File Sizes
- **DMG**: ~150-300 MB (يعتمد على المحتوى)
- **DMG**: ~150-300 MB (depends on content)

### للمطورين / For Developers
إذا كنت تريد تخصيص البناء، يمكنك تعديل:
If you want to customize the build, you can modify:

- `package.json` - إعدادات البناء / Build configuration
- `build/entitlements.mac.plist` - صلاحيات macOS / macOS entitlements
- `assets/` - الرموز والخلفيات / Icons and backgrounds

## الخطوات التالية / Next Steps

1. **اختبار التطبيق**: تأكد من عمل التطبيق بشكل صحيح
2. **Test Application**: Ensure the app works correctly
3. **التوزيع**: رفع الملف أو توزيعه
4. **Distribution**: Upload or distribute the file
5. **التوقيع الرقمي**: للتوزيع عبر Mac App Store
6. **Code Signing**: For Mac App Store distribution

---

**ملاحظة مهمة**: تأكد من تثبيت Python 3 على الأجهزة المستهدفة لتشغيل الخادم الخلفي.
**Important Note**: Ensure Python 3 is installed on target machines to run the backend server.
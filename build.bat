@echo off
REM Hospital Management System Desktop Build Script for Windows
REM Builds the application for Windows platform

setlocal enabledelayedexpansion

echo 🏥 Hospital Management System - Windows Build Script
echo ====================================================

REM Check if we're in the desktop directory
if not exist package.json (
    echo [ERROR] package.json not found. Please run this script from the desktop directory.
    exit /b 1
)

REM Check for npm
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed. Please install Node.js and npm first.
    exit /b 1
)

REM Install dependencies if needed
if not exist node_modules (
    echo [INFO] Installing Node.js dependencies...
    npm install
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install dependencies
        exit /b 1
    )
    echo [SUCCESS] Dependencies installed
) else (
    echo [INFO] Node.js dependencies already installed
)

REM Create placeholder icons if they don't exist
echo [INFO] Setting up build assets...

if not exist assets mkdir assets
if not exist build mkdir build

REM Create a simple icon placeholder (this should be replaced with actual icons)
if not exist assets\icon.ico (
    echo [INFO] Creating placeholder Windows icon...
    REM In a real scenario, you would copy or generate proper icon files here
    echo. > assets\icon.ico
)

REM Build for Windows
echo [INFO] Building Windows application...
npm run build:win

if %errorlevel% equ 0 (
    echo [SUCCESS] Windows build completed!
    
    REM Show results
    if exist dist (
        echo.
        echo [SUCCESS] Build completed! Output files:
        dir dist\*.exe /s /b 2>nul
        echo.
        echo 📋 Windows installer created in dist/ directory
    )
) else (
    echo [ERROR] Windows build failed
    exit /b 1
)

echo.
echo 🎉 Windows desktop application build process completed!
echo.
echo 📋 Files created:
echo   - Hospital Management System Setup.exe (Installer)
echo   - Hospital Management System.exe (Portable version)
echo.
echo 💡 Tip: Test the application on different Windows versions before distribution

pause
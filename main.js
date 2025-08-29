const { app, BrowserWindow, Menu, shell, dialog, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const axios = require('axios');
const log = require('electron-log');

// Configure logging
log.transports.file.level = 'info';
log.transports.console.level = 'debug';

class HospitalManagementApp {
    constructor() {
        this.mainWindow = null;
        this.backendProcess = null;
        this.serverPort = 8000;
        this.serverUrl = `http://localhost:${this.serverPort}`;
        this.isQuitting = false;

        // Set up event listeners
        this.setupAppEventListeners();
        this.setupIpcHandlers();
    }

    setupAppEventListeners() {
        app.whenReady().then(() => {
            this.createWindow();
            this.startBackendServer();

            app.on('activate', () => {
                if (BrowserWindow.getAllWindows().length === 0) {
                    this.createWindow();
                }
            });
        });

        app.on('window-all-closed', () => {
            this.isQuitting = true;
            this.stopBackendServer();
            if (process.platform !== 'darwin') {
                app.quit();
            }
        });

        app.on('before-quit', () => {
            this.isQuitting = true;
            this.stopBackendServer();
        });
    }

    setupIpcHandlers() {
        // Handle server status requests
        ipcMain.handle('check-server-status', async() => {
            return this.checkServerStatus();
        });

        // Handle server restart
        ipcMain.handle('restart-server', async() => {
            this.stopBackendServer();
            await this.delay(2000);
            return this.startBackendServer();
        });

        // Handle opening external links
        ipcMain.handle('open-external', async(event, url) => {
            shell.openExternal(url);
        });
    }

    createWindow() {
        // Create the browser window
        this.mainWindow = new BrowserWindow({
            width: 1400,
            height: 900,
            minWidth: 1200,
            minHeight: 800,
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true,
                enableRemoteModule: false,
                preload: path.join(__dirname, 'preload.js')
            },
            icon: this.getIconPath(),
            title: 'Hospital Management System',
            titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
            show: false // Don't show until ready
        });

        // Set up window event listeners
        this.mainWindow.once('ready-to-show', () => {
            this.mainWindow.show();

            if (process.env.NODE_ENV === 'development') {
                this.mainWindow.webContents.openDevTools();
            }
        });

        this.mainWindow.on('closed', () => {
            this.mainWindow = null;
        });

        // Load the loading page first
        this.mainWindow.loadFile(path.join(__dirname, 'loading.html'));

        // Wait for server to be ready, then load the app
        this.waitForServerAndLoad();

        // Create application menu
        this.createMenu();
    }

    async waitForServerAndLoad() {
        let attempts = 0;
        const maxAttempts = 30;

        const checkServer = async() => {
            try {
                const response = await axios.get(`${this.serverUrl}/health`, { timeout: 2000 });
                if (response.status === 200) {
                    log.info('Backend server is ready');
                    this.mainWindow.loadURL(this.serverUrl);
                    return;
                }
            } catch (error) {
                // Server not ready yet
            }

            attempts++;
            if (attempts < maxAttempts) {
                setTimeout(checkServer, 2000);
            } else {
                log.error('Backend server failed to start');
                this.showServerError();
            }
        };

        checkServer();
    }

    startBackendServer() {
        return new Promise((resolve, reject) => {
            try {
                const backendPath = this.getBackendPath();
                const pythonExecutable = this.findPythonExecutable();

                log.info(`Starting backend server from: ${backendPath}`);
                log.info(`Using Python: ${pythonExecutable}`);

                // Start the Python backend
                this.backendProcess = spawn(pythonExecutable, ['start.py'], {
                    cwd: backendPath,
                    env: {
                        ...process.env,
                        PYTHONPATH: backendPath,
                        HMS_DESKTOP_MODE: 'true'
                    },
                    stdio: ['ignore', 'pipe', 'pipe']
                });

                this.backendProcess.stdout.on('data', (data) => {
                    log.info(`Backend: ${data.toString()}`);
                });

                this.backendProcess.stderr.on('data', (data) => {
                    log.error(`Backend Error: ${data.toString()}`);
                });

                this.backendProcess.on('close', (code) => {
                    log.info(`Backend process exited with code ${code}`);
                    if (!this.isQuitting && code !== 0) {
                        this.showServerError();
                    }
                });

                resolve(true);

            } catch (error) {
                log.error('Failed to start backend server:', error);
                reject(error);
            }
        });
    }

    stopBackendServer() {
        if (this.backendProcess) {
            log.info('Stopping backend server...');
            this.backendProcess.kill('SIGTERM');
            this.backendProcess = null;
        }
    }

    async checkServerStatus() {
        try {
            const response = await axios.get(`${this.serverUrl}/health`, { timeout: 5000 });
            return { status: 'running', data: response.data };
        } catch (error) {
            return { status: 'stopped', error: error.message };
        }
    }

    showServerError() {
        const options = {
            type: 'error',
            title: 'Server Error',
            message: 'Hospital Management System Backend Failed to Start',
            detail: 'The backend server could not be started. Please check that Python and all dependencies are installed correctly.',
            buttons: ['Retry', 'Open Logs', 'Quit'],
            defaultId: 0
        };

        dialog.showMessageBox(this.mainWindow, options).then((response) => {
            switch (response.response) {
                case 0: // Retry
                    this.startBackendServer();
                    this.waitForServerAndLoad();
                    break;
                case 1: // Open Logs
                    shell.openPath(log.transports.file.getFile().path);
                    break;
                case 2: // Quit
                    app.quit();
                    break;
            }
        });
    }

    createMenu() {
        const template = [{
                label: 'File',
                submenu: [{
                        label: 'New Patient',
                        accelerator: 'CmdOrCtrl+N',
                        click: () => {
                            this.mainWindow.webContents.send('navigate-to', '/patients/new');
                        }
                    },
                    {
                        label: 'Search',
                        accelerator: 'CmdOrCtrl+F',
                        click: () => {
                            this.mainWindow.webContents.send('focus-search');
                        }
                    },
                    { type: 'separator' },
                    {
                        label: 'Quit',
                        accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
                        click: () => {
                            app.quit();
                        }
                    }
                ]
            },
            {
                label: 'View',
                submenu: [{
                        label: 'Dashboard',
                        accelerator: 'CmdOrCtrl+1',
                        click: () => {
                            this.mainWindow.webContents.send('navigate-to', '/');
                        }
                    },
                    {
                        label: 'Patients',
                        accelerator: 'CmdOrCtrl+2',
                        click: () => {
                            this.mainWindow.webContents.send('navigate-to', '/patients');
                        }
                    },
                    {
                        label: 'Doctors',
                        accelerator: 'CmdOrCtrl+3',
                        click: () => {
                            this.mainWindow.webContents.send('navigate-to', '/doctors');
                        }
                    },
                    { type: 'separator' },
                    {
                        label: 'Toggle Language',
                        accelerator: 'CmdOrCtrl+L',
                        click: () => {
                            this.mainWindow.webContents.send('toggle-language');
                        }
                    },
                    {
                        label: 'Toggle Theme',
                        accelerator: 'CmdOrCtrl+T',
                        click: () => {
                            this.mainWindow.webContents.send('toggle-theme');
                        }
                    },
                    { type: 'separator' },
                    {
                        label: 'Reload',
                        accelerator: 'CmdOrCtrl+R',
                        click: () => {
                            this.mainWindow.reload();
                        }
                    },
                    {
                        label: 'Force Reload',
                        accelerator: 'CmdOrCtrl+Shift+R',
                        click: () => {
                            this.mainWindow.webContents.reloadIgnoringCache();
                        }
                    },
                    {
                        label: 'Toggle Developer Tools',
                        accelerator: process.platform === 'darwin' ? 'Alt+Cmd+I' : 'Ctrl+Shift+I',
                        click: () => {
                            this.mainWindow.webContents.toggleDevTools();
                        }
                    }
                ]
            },
            {
                label: 'Server',
                submenu: [{
                        label: 'Server Status',
                        click: () => {
                            this.mainWindow.webContents.send('check-server-status');
                        }
                    },
                    {
                        label: 'Restart Server',
                        click: () => {
                            this.mainWindow.webContents.send('restart-server');
                        }
                    },
                    { type: 'separator' },
                    {
                        label: 'Open API Documentation',
                        click: () => {
                            shell.openExternal(`${this.serverUrl}/docs`);
                        }
                    }
                ]
            },
            {
                label: 'Help',
                submenu: [{
                        label: 'About Hospital Management System',
                        click: () => {
                            this.showAboutDialog();
                        }
                    },
                    {
                        label: 'Setup Guide',
                        click: () => {
                            shell.openExternal('file://' + path.join(this.getBackendPath(), 'SETUP_GUIDE.md'));
                        }
                    },
                    {
                        label: 'Report Issue',
                        click: () => {
                            shell.openExternal('mailto:support@hospital-system.com');
                        }
                    }
                ]
            }
        ];

        // macOS specific menu adjustments
        if (process.platform === 'darwin') {
            template.unshift({
                label: app.getName(),
                submenu: [{
                        label: 'About ' + app.getName(),
                        click: () => {
                            this.showAboutDialog();
                        }
                    },
                    { type: 'separator' },
                    {
                        label: 'Services',
                        role: 'services',
                        submenu: []
                    },
                    { type: 'separator' },
                    {
                        label: 'Hide ' + app.getName(),
                        accelerator: 'Command+H',
                        role: 'hide'
                    },
                    {
                        label: 'Hide Others',
                        accelerator: 'Command+Shift+H',
                        role: 'hideothers'
                    },
                    {
                        label: 'Show All',
                        role: 'unhide'
                    },
                    { type: 'separator' },
                    {
                        label: 'Quit',
                        accelerator: 'Command+Q',
                        click: () => {
                            app.quit();
                        }
                    }
                ]
            });

            // Remove quit from file menu on macOS
            template[1].submenu.pop();
        }

        const menu = Menu.buildFromTemplate(template);
        Menu.setApplicationMenu(menu);
    }

    showAboutDialog() {
        const options = {
            type: 'info',
            title: 'About Hospital Management System',
            message: 'Hospital Management System',
            detail: `Version: 1.0.0
Comprehensive healthcare management platform with bilingual support (Arabic/English).

Features:
• Patient Management
• Doctor Registration  
• Emergency Department
• Laboratory & Radiology
• Pharmacy Management
• Financial Management
• Human Resources
• Warehouse Management

Copyright © 2024 Hospital Management System Team`,
            buttons: ['OK']
        };

        dialog.showMessageBox(this.mainWindow, options);
    }

    getBackendPath() {
        if (process.env.NODE_ENV === 'development') {
            return path.join(__dirname, '../../');
        } else {
            return path.join(process.resourcesPath, 'backend');
        }
    }

    findPythonExecutable() {
        const possiblePaths = ['python3', 'python', 'py'];

        // In development, try common Python paths
        if (process.env.NODE_ENV === 'development') {
            return 'python3';
        }

        // In production, Python should be bundled or available in PATH
        return 'python3';
    }

    getIconPath() {
        const iconName = process.platform === 'win32' ? 'icon.ico' :
            process.platform === 'darwin' ? 'icon.icns' : 'icon.png';
        return path.join(__dirname, '../assets', iconName);
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize the application
new HospitalManagementApp();
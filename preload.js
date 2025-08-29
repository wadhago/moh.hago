const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
    // Server management
    checkServerStatus: () => ipcRenderer.invoke('check-server-status'),
    restartServer: () => ipcRenderer.invoke('restart-server'),
    
    // External links
    openExternal: (url) => ipcRenderer.invoke('open-external', url),
    
    // Navigation
    onNavigateTo: (callback) => ipcRenderer.on('navigate-to', callback),
    onFocusSearch: (callback) => ipcRenderer.on('focus-search', callback),
    onToggleLanguage: (callback) => ipcRenderer.on('toggle-language', callback),
    onToggleTheme: (callback) => ipcRenderer.on('toggle-theme', callback),
    onCheckServerStatus: (callback) => ipcRenderer.on('check-server-status', callback),
    onRestartServer: (callback) => ipcRenderer.on('restart-server', callback),
    
    // System info
    platform: process.platform,
    
    // Remove listeners
    removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel)
});
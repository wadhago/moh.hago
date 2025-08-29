// Desktop Enhancement Script for Hospital Management System
// This script adds desktop-specific functionality when running in Electron

class DesktopEnhancements {
    constructor() {
        this.isElectron = window.electronAPI !== undefined;
        this.init();
    }

    init() {
        if (!this.isElectron) return;

        console.log('🖥️ Desktop mode detected - Initializing enhancements...');

        // Set up desktop-specific features
        this.setupKeyboardShortcuts();
        this.setupDesktopNavigation();
        this.setupDesktopMenuHandlers();
        this.setupServerStatusMonitoring();
        this.addDesktopIndicator();

        // Enhance existing hospital app
        this.enhanceHospitalApp();
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Prevent default browser shortcuts in desktop mode
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case 'r':
                        if (e.shiftKey) {
                            e.preventDefault();
                            location.reload();
                        }
                        break;
                    case 'w':
                        e.preventDefault(); // Prevent closing tab
                        break;
                    case 't':
                        e.preventDefault(); // Prevent new tab
                        break;
                }
            }
        });
    }

    setupDesktopNavigation() {
        // Listen for navigation commands from menu
        window.electronAPI.onNavigateTo((event, path) => {
            this.navigateToPath(path);
        });

        // Focus search when requested
        window.electronAPI.onFocusSearch(() => {
            const searchInput = document.querySelector('input[type="search"]');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        });

        // Toggle language
        window.electronAPI.onToggleLanguage(() => {
            if (window.hospitalApp && window.hospitalApp.toggleLanguage) {
                window.hospitalApp.toggleLanguage();
            }
        });

        // Toggle theme
        window.electronAPI.onToggleTheme(() => {
            if (window.hospitalApp && window.hospitalApp.toggleTheme) {
                window.hospitalApp.toggleTheme();
            }
        });
    }

    setupDesktopMenuHandlers() {
        // Handle server status check from menu
        window.electronAPI.onCheckServerStatus(async() => {
            const status = await window.electronAPI.checkServerStatus();
            this.showServerStatusDialog(status);
        });

        // Handle server restart from menu
        window.electronAPI.onRestartServer(async() => {
            this.showServerRestartDialog();
        });
    }

    async setupServerStatusMonitoring() {
        // Check server status periodically
        setInterval(async() => {
            try {
                const status = await window.electronAPI.checkServerStatus();
                this.updateServerStatusIndicator(status.status === 'running');
            } catch (error) {
                this.updateServerStatusIndicator(false);
            }
        }, 30000); // Check every 30 seconds
    }

    addDesktopIndicator() {
        // Add desktop mode indicator to header
        const header = document.querySelector('.header-right');
        if (header) {
            const desktopIndicator = document.createElement('div');
            desktopIndicator.className = 'desktop-indicator';
            desktopIndicator.innerHTML = `
                <div class="indicator-badge" title="Desktop Mode">
                    🖥️ <span class="server-status" id="server-status-dot">●</span>
                </div>
            `;
            desktopIndicator.style.cssText = `
                display: flex;
                align-items: center;
                font-size: 0.875rem;
                color: var(--text-secondary);
                margin-right: 1rem;
            `;

            const statusStyle = document.createElement('style');
            statusStyle.textContent = `
                .desktop-indicator .indicator-badge {
                    display: flex;
                    align-items: center;
                    gap: 0.25rem;
                    padding: 0.25rem 0.5rem;
                    background: rgba(37, 99, 235, 0.1);
                    border-radius: 4px;
                    font-size: 0.75rem;
                }
                
                .server-status {
                    font-size: 0.5rem;
                    color: #10b981;
                    animation: pulse 2s infinite;
                }
                
                .server-status.offline {
                    color: #ef4444;
                }
                
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
            `;
            document.head.appendChild(statusStyle);
            header.prepend(desktopIndicator);
        }
    }

    enhanceHospitalApp() {
        // Wait for hospital app to be available
        const checkHospitalApp = () => {
            if (window.hospitalApp) {
                this.addDesktopMethodsToHospitalApp();
            } else {
                setTimeout(checkHospitalApp, 100);
            }
        };
        checkHospitalApp();
    }

    addDesktopMethodsToHospitalApp() {
        const hospitalApp = window.hospitalApp;

        // Override notification method for desktop
        const originalShowNotification = hospitalApp.showNotification.bind(hospitalApp);
        hospitalApp.showNotification = (message, type = 'info') => {
            originalShowNotification(message, type);

            // Also show desktop notification for important messages
            if (type === 'error' || type === 'success') {
                this.showDesktopNotification(message, type);
            }
        };

        // Add desktop-specific methods
        hospitalApp.openExternal = (url) => {
            window.electronAPI.openExternal(url);
        };

        hospitalApp.checkServerStatus = async() => {
            return await window.electronAPI.checkServerStatus();
        };

        hospitalApp.restartServer = async() => {
            return await window.electronAPI.restartServer();
        };
    }

    navigateToPath(path) {
        // Simple client-side navigation
        window.location.hash = path;
        window.location.pathname = path;
    }

    updateServerStatusIndicator(isOnline) {
        const statusDot = document.getElementById('server-status-dot');
        if (statusDot) {
            statusDot.className = isOnline ? 'server-status' : 'server-status offline';
            statusDot.title = isOnline ? 'Server Online' : 'Server Offline';
        }
    }

    showServerStatusDialog(status) {
            const modal = this.createModal('Server Status', `
            <div style="padding: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                    <span style="font-size: 1.5rem;">${status.status === 'running' ? '🟢' : '🔴'}</span>
                    <strong>Status: ${status.status === 'running' ? 'Online' : 'Offline'}</strong>
                </div>
                ${status.status === 'running' ? `
                    <p><strong>Application:</strong> ${status.data?.app || 'N/A'}</p>
                    <p><strong>Version:</strong> ${status.data?.version || 'N/A'}</p>
                ` : `
                    <p style="color: #ef4444;"><strong>Error:</strong> ${status.error || 'Server not responding'}</p>
                `}
            </div>
        `);
        
        this.showModal(modal);
    }

    showServerRestartDialog() {
        const modal = this.createModal('Restart Server', `
            <div style="padding: 1rem;">
                <p>Are you sure you want to restart the backend server?</p>
                <p style="color: #f59e0b; font-size: 0.875rem; margin-top: 0.5rem;">
                    This will temporarily disconnect the application.
                </p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; justify-content: flex-end;">
                    <button class="btn btn-outline" onclick="this.closest('.modal-overlay').remove()">
                        Cancel
                    </button>
                    <button class="btn btn-primary" onclick="window.desktopEnhancements.performServerRestart()">
                        Restart Server
                    </button>
                </div>
            </div>
        `);
        
        this.showModal(modal);
    }

    async performServerRestart() {
        // Close the modal
        document.querySelector('.modal-overlay')?.remove();
        
        // Show progress
        const progressModal = this.createModal('Restarting Server', `
            <div style="padding: 2rem; text-align: center;">
                <div class="loading-spinner" style="margin: 0 auto 1rem;"></div>
                <p>Restarting backend server...</p>
                <p style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.5rem;">
                    Please wait while the server restarts.
                </p>
            </div>
        `);
        
        this.showModal(progressModal);
        
        try {
            await window.electronAPI.restartServer();
            
            // Wait a bit for server to restart
            setTimeout(() => {
                document.querySelector('.modal-overlay')?.remove();
                location.reload();
            }, 3000);
            
        } catch (error) {
            document.querySelector('.modal-overlay')?.remove();
            this.showDesktopNotification('Failed to restart server', 'error');
        }
    }

    createModal(title, content) {
        return `
            <div class="modal-overlay" style="
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
            ">
                <div class="modal" style="
                    background: var(--surface-color);
                    border-radius: var(--border-radius);
                    box-shadow: var(--shadow-lg);
                    min-width: 300px;
                    max-width: 500px;
                ">
                    <div class="modal-header" style="
                        padding: 1rem 1.5rem;
                        border-bottom: 1px solid var(--border-color);
                        font-weight: 600;
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                    ">
                        ${title}
                        <button onclick="this.closest('.modal-overlay').remove()" style="
                            background: none;
                            border: none;
                            font-size: 1.25rem;
                            cursor: pointer;
                            color: var(--text-secondary);
                        ">×</button>
                    </div>
                    <div class="modal-content">
                        ${content}
                    </div>
                </div>
            </div>
        `;
    }

    showModal(modalHTML) {
        // Remove existing modals
        document.querySelectorAll('.modal-overlay').forEach(modal => modal.remove());
        
        // Add new modal
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Close on outside click
        document.querySelector('.modal-overlay').addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-overlay')) {
                e.target.remove();
            }
        });
    }

    showDesktopNotification(message, type) {
        // This would show a native desktop notification
        // For now, we'll enhance the existing web notification
        console.log(`Desktop notification: ${type.toUpperCase()} - ${message}`);
    }
}

// Initialize desktop enhancements when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.desktopEnhancements = new DesktopEnhancements();
});

// Also initialize if DOM is already loaded
if (document.readyState === 'loading') {
    // DOM not ready yet
} else {
    window.desktopEnhancements = new DesktopEnhancements();
}
// ===== АУТЕНТИФИКАЦИЯ =====
const Auth = {
    init() {
        this.checkAuth();
        this.setupEventListeners();
    },

    checkAuth() {
        const publicPages = ['/login.html', '/index.html', '/', '/register.html', '/pages/create-request.html'];
        const currentPath = window.location.pathname;

        if (!publicPages.includes(currentPath) && !StorageManager.isAuthenticated()) {
            window.location.href = '/login.html';
        }
    },

    setupEventListeners() {
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.logout());
        }
    },

    async login(login, password) {
        try {
            const response = await fetch(`${API_BASE}/Auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ login, password })
            });

            await ErrorHandler.handle(response);
            const data = await response.json();

            StorageManager.setUser(data.user);
            if (data.token) {
                StorageManager.setToken(data.token);
            }

            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    async register(userData) {
        try {
            const response = await fetch(`${API_BASE}/Auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });

            await ErrorHandler.handle(response);
            const data = await response.json();

            return { success: true, data };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    async checkLogin(login) {
        try {
            const response = await fetch(`${API_BASE}/Auth/check/${login}`);
            const data = await response.json();
            return data.exists;
        } catch {
            return false;
        }
    },

    logout() {
        StorageManager.removeUser();
        window.location.href = '/login.html';
    },

    getCurrentUser() {
        return StorageManager.getUser();
    },

    hasRole(role) {
        const user = this.getCurrentUser();
        return user && user.type === role;
    },

    isManager() {
        const user = this.getCurrentUser();
        return user && (user.type === 'Менеджер' || user.type === 'Менеджер по качеству');
    },

    isMaster() {
        const user = this.getCurrentUser();
        return user && user.type === 'Специалист';
    },

    isClient() {
        const user = this.getCurrentUser();
        return user && user.type === 'Заказчик';
    }
};

// Делаем Auth глобальным
window.Auth = Auth;

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => Auth.init());
// ===== КОНСТАНТЫ =====
const API_BASE = 'https://localhost:7233/api';

// ===== УПРАВЛЕНИЕ СООБЩЕНИЯМИ =====
const NotificationManager = {
    show(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `message ${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button onclick="this.parentElement.remove()" style="background: none; border: none; cursor: pointer; margin-left: 1rem;">✕</button>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, duration);
    },

    success(message) { this.show(message, 'success'); },
    error(message) { this.show(message, 'error'); },
    warning(message) { this.show(message, 'warning'); },
    info(message) { this.show(message, 'info'); }
};

// ===== РАБОТА С LOCALSTORAGE =====
const StorageManager = {
    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    setUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
    },

    removeUser() {
        localStorage.removeItem('user');
        localStorage.removeItem('token');
    },

    getToken() {
        return localStorage.getItem('token');
    },

    setToken(token) {
        localStorage.setItem('token', token);
    },

    isAuthenticated() {
        return !!this.getUser();
    }
};

// ===== ФОРМАТИРОВАНИЕ =====
const Formatter = {
    date(date) {
        if (!date) return '—';
        return new Date(date).toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    datetime(date) {
        if (!date) return '—';
        return new Date(date).toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    phone(phone) {
        if (!phone) return '—';
        // Простое форматирование
        return phone;
    },

    days(days) {
        if (days === null || days === undefined) return '—';

        const absDays = Math.abs(days);
        let text;

        if (absDays % 10 === 1 && absDays % 100 !== 11) {
            text = 'день';
        } else if ([2, 3, 4].includes(absDays % 10) && ![12, 13, 14].includes(absDays % 100)) {
            text = 'дня';
        } else {
            text = 'дней';
        }

        return `${days} ${text}`;
    }
};

// ===== ОБРАБОТКА ОШИБОК =====
const ErrorHandler = {
    async handle(response) {
        if (!response.ok) {
            let message = 'Произошла ошибка';
            try {
                const data = await response.json();
                message = data.message || message;
            } catch {
                message = response.statusText || message;
            }
            throw new Error(message);
        }
        return response;
    }
};

// Делаем объекты глобальными
window.NotificationManager = NotificationManager;
window.StorageManager = StorageManager;
window.Formatter = Formatter;
window.ErrorHandler = ErrorHandler;
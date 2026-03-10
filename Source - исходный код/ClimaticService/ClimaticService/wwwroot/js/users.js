/**
 * API и утилиты для страницы «Пользователи».
 * Редактирование и удаление доступны только менеджеру (проверка на бэкенде).
 */

const UsersAPI = {
    /** Загрузка списка пользователей */
    async getAll() {
        const response = await fetch(`${API_BASE}/Auth/users`);
        await ErrorHandler.handle(response);
        return response.json();
    },

    /**
     * Обновление пользователя. Требуется заголовок X-Current-User-Id (только менеджер).
     * @param {number} id - ID пользователя
     * @param {Object} data - { fio, phone, login, password?, type }
     */
    async update(id, data) {
        const user = StorageManager.getUser();
        if (!user || !user.userId) throw new Error('Необходима авторизация');

        const response = await fetch(`${API_BASE}/Auth/users/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-Current-User-Id': String(user.userId)
            },
            body: JSON.stringify({
                Fio: data.fio,
                Phone: data.phone,
                Login: data.login,
                Password: data.password || null,
                Type: data.type
            })
        });
        await ErrorHandler.handle(response);
        return response.json();
    },

    /**
     * Мягкое удаление пользователя. Только менеджер.
     */
    async delete(id) {
        const user = StorageManager.getUser();
        if (!user || !user.userId) throw new Error('Необходима авторизация');

        const response = await fetch(`${API_BASE}/Auth/users/${id}`, {
            method: 'DELETE',
            headers: { 'X-Current-User-Id': String(user.userId) }
        });
        await ErrorHandler.handle(response);
        return response.json();
    }
};

window.UsersAPI = UsersAPI;

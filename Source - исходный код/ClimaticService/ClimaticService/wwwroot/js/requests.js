// ===== РАБОТА С ЗАЯВКАМИ =====
const RequestsAPI = {
    // ===== ПОЛУЧЕНИЕ ДАННЫХ =====
    async getAll() {
        const response = await fetch(`${API_BASE}/Requests`);
        await ErrorHandler.handle(response);
        return response.json();
    },

    async getById(id) {
        const response = await fetch(`${API_BASE}/Requests/${id}`);
        await ErrorHandler.handle(response);
        return response.json();
    },

    async getClientRequests(clientId) {
        const response = await fetch(`${API_BASE}/Requests/client/${clientId}`);
        await ErrorHandler.handle(response);
        return response.json();
    },

    async getMasterRequests(masterId) {
        const response = await fetch(`${API_BASE}/Requests/master/${masterId}`);
        await ErrorHandler.handle(response);
        return response.json();
    },

    async getTypes() {
        const response = await fetch(`${API_BASE}/Requests/types`);
        await ErrorHandler.handle(response);
        return response.json();
    },

    async getStatuses() {
        const response = await fetch(`${API_BASE}/Requests/statuses`);
        await ErrorHandler.handle(response);
        return response.json();
    },

    async getStatistics() {
        const response = await fetch(`${API_BASE}/Requests/statistics`);
        await ErrorHandler.handle(response);
        return response.json();
    },

    async getComments(requestId) {
        const response = await fetch(`${API_BASE}/Requests/${requestId}/comments`);
        await ErrorHandler.handle(response);
        return response.json();
    },

    // ===== СОЗДАНИЕ И РЕДАКТИРОВАНИЕ =====
    async create(data) {
        const response = await fetch(`${API_BASE}/Requests`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        await ErrorHandler.handle(response);
        return response.json();
    },

    async update(id, data) {
        const response = await fetch(`${API_BASE}/Requests/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        await ErrorHandler.handle(response);
        return response.json();
    },

    async delete(id) {
        const response = await fetch(`${API_BASE}/Requests/${id}`, { method: 'DELETE' });
        await ErrorHandler.handle(response);
    },

    // ===== ДЕЙСТВИЯ С ЗАЯВКАМИ =====
    async changeStatus(id, statusId) {
        const response = await fetch(`${API_BASE}/Requests/${id}/status/${statusId}`, {
            method: 'POST'
        });
        await ErrorHandler.handle(response);
        return response.json();
    },

    async assignMaster(id, masterId) {
        const response = await fetch(`${API_BASE}/Requests/${id}/assign-master/${masterId}`, {
            method: 'POST'
        });
        await ErrorHandler.handle(response);
        return response.json();
    },

    async addComment(id, message, masterId) {
        const response = await fetch(`${API_BASE}/Requests/${id}/comments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, masterId })
        });
        await ErrorHandler.handle(response);
        return response.json();
    },

    async requestQualityHelp(id, data) {
        const response = await fetch(`${API_BASE}/Requests/${id}/quality-help`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        await ErrorHandler.handle(response);
        return response.json();
    },

    async extendDeadline(id, data) {
        const response = await fetch(`${API_BASE}/Requests/${id}/extend-deadline`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        await ErrorHandler.handle(response);
        return response.json();
    },

    // ===== ПОИСК =====
    async search(params) {
        const response = await fetch(`${API_BASE}/Requests/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });
        await ErrorHandler.handle(response);
        return response.json();
    }
};

// ===== КОМПОНЕНТЫ ДЛЯ ОТОБРАЖЕНИЯ =====
const RequestRenderer = {
    getStatusClass(statusName) {
        const statusMap = {
            'Новая заявка': 'status-new',
            'В процессе ремонта': 'status-progress',
            'Ожидание комплектующих': 'status-waiting',
            'Завершена': 'status-completed',
            'Отменена': 'status-cancelled'
        };
        return statusMap[statusName] || 'status-new';
    },

    formatRequest(request) {
        const daysInWork = request.startDate
            ? Math.ceil((new Date() - new Date(request.startDate)) / (1000 * 60 * 60 * 24))
            : 0;

        return {
            ...request,
            formattedStartDate: Formatter.date(request.startDate),
            formattedCompletionDate: Formatter.date(request.completionDate),
            daysInWork,
            statusClass: this.getStatusClass(request.status?.statusName)
        };
    },

    renderTableRow(request, options = {}) {
        const { actions = true, showDelete = false } = typeof options === 'boolean' ? { actions: options } : options;
        const formatted = this.formatRequest(request);

        return `
            <tr onclick="window.location.href='/pages/request-detail.html?id=${request.requestId}'">
                <td>#${request.requestId}</td>
                <td>${formatted.formattedStartDate}</td>
                <td>${request.equipmentType?.typeName || '—'}</td>
                <td>${request.model}</td>
                <td>${request.client?.fio || '—'}</td>
                <td>
                    <span class="status-badge ${formatted.statusClass}">
                        ${request.status?.statusName || '—'}
                    </span>
                </td>
                <td>${request.master?.fio || '—'}</td>
                <td>${Formatter.days(formatted.daysInWork)}</td>
                ${actions ? `
                    <td onclick="event.stopPropagation()">
                        <div style="display: flex; gap: 0.5rem;">
                            <button class="btn btn-sm" onclick="window.location.href='/pages/edit-request.html?id=${request.requestId}'" title="редактировать">✎</button>
                            ${showDelete ? `<button class="btn btn-sm btn-danger" onclick="window.deleteRequestConfirm(${request.requestId}, this)" title="удалить">🗑</button>` : ''}
                        </div>
                    </td>
                ` : ''}
            </tr>
        `;
    }
};

// Делаем объекты глобальными
window.RequestsAPI = RequestsAPI;
window.RequestRenderer = RequestRenderer;
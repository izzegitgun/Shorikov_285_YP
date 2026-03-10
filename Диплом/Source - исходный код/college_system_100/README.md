## Навигация по репозиторию

Папка: `college_system/`

- `college_system/config/` — настройки Django, `urls.py`, `wsgi.py`, `asgi.py`
- `college_system/apps/` — Django-приложения
  - `apps/authentication/` — пользователи/аутентификация
  - `apps/core/` — основная логика системы
- `college_system/templates/` — общие шаблоны
- `college_system/static/` — статика
- `college_system/data/` — локальная SQLite БД (`db.sqlite3`) при `USE_SQLITE_FOR_DEV=True`
- `college_system/logs/` — логи приложения
- `college_system/scripts/sql/` — SQL-скрипты
- `college_system/docs/diagrams/` — диаграммы/документация

Инструкции запуска — в `college_system/console_manager.py`.



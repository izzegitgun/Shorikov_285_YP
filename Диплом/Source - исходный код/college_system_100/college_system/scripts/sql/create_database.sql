-- =====================================================
-- SQL скрипт для создания базы данных College System
-- База данных: SQLite
-- =====================================================

-- Включение поддержки внешних ключей
PRAGMA foreign_keys = ON;

-- =====================================================
-- Таблица: auth_user (User)
-- Описание: Пользователи системы с ролями
-- =====================================================
CREATE TABLE IF NOT EXISTS auth_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOLEAN NOT NULL DEFAULT 0,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    date_joined DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(20) NOT NULL DEFAULT 'teacher' CHECK(role IN ('admin', 'accountant', 'curator', 'teacher'))
);

-- Индексы для таблицы auth_user
CREATE INDEX IF NOT EXISTS idx_auth_user_username ON auth_user(username);
CREATE INDEX IF NOT EXISTS idx_auth_user_email ON auth_user(email);
CREATE INDEX IF NOT EXISTS idx_auth_user_role ON auth_user(role);

-- =====================================================
-- Таблица: core_teacher (Teacher)
-- Описание: Преподаватели
-- =====================================================
CREATE TABLE IF NOT EXISTS core_teacher (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    academic_degree VARCHAR(50) NOT NULL,
    rate DECIMAL(10, 2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- Индексы для таблицы core_teacher
CREATE INDEX IF NOT EXISTS idx_core_teacher_user_id ON core_teacher(user_id);
CREATE INDEX IF NOT EXISTS idx_core_teacher_is_active ON core_teacher(is_active);

-- =====================================================
-- Таблица: core_subject (Subject)
-- Описание: Учебные дисциплины/предметы
-- =====================================================
CREATE TABLE IF NOT EXISTS core_subject (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL,
    code VARCHAR(50) DEFAULT '',
    description TEXT DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT 1
);

-- Индексы для таблицы core_subject
CREATE INDEX IF NOT EXISTS idx_core_subject_name ON core_subject(name);
CREATE INDEX IF NOT EXISTS idx_core_subject_is_active ON core_subject(is_active);

-- =====================================================
-- Таблица: core_studygroup (StudyGroup)
-- Описание: Учебные группы
-- =====================================================
CREATE TABLE IF NOT EXISTS core_studygroup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT 1
);

-- Индексы для таблицы core_studygroup
CREATE INDEX IF NOT EXISTS idx_core_studygroup_name ON core_studygroup(name);
CREATE INDEX IF NOT EXISTS idx_core_studygroup_is_active ON core_studygroup(is_active);

-- =====================================================
-- Таблица: core_workload (Workload)
-- Описание: Учебная нагрузка/расписание занятий
-- =====================================================
CREATE TABLE IF NOT EXISTS core_workload (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    group_id INTEGER,
    date DATE NOT NULL,
    activity_type VARCHAR(50) NOT NULL CHECK(activity_type IN ('lecture', 'practice', 'lab')),
    pair_slot VARCHAR(1) DEFAULT '' CHECK(pair_slot IN ('', '1', '2', '3', '4', '5', '6')),
    description TEXT DEFAULT '',
    FOREIGN KEY (teacher_id) REFERENCES core_teacher(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES core_subject(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES core_studygroup(id) ON DELETE CASCADE
);

-- Индексы для таблицы core_workload
CREATE INDEX IF NOT EXISTS idx_core_workload_teacher_id ON core_workload(teacher_id);
CREATE INDEX IF NOT EXISTS idx_core_workload_subject_id ON core_workload(subject_id);
CREATE INDEX IF NOT EXISTS idx_core_workload_group_id ON core_workload(group_id);
CREATE INDEX IF NOT EXISTS idx_core_workload_date ON core_workload(date);
CREATE INDEX IF NOT EXISTS idx_core_workload_activity_type ON core_workload(activity_type);

-- =====================================================
-- Таблица: core_timesheet (Timesheet)
-- Описание: Табели учета рабочего времени
-- =====================================================
CREATE TABLE IF NOT EXISTS core_timesheet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    period DATE NOT NULL,
    total_hours DECIMAL(8, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'draft' CHECK(status IN ('draft', 'approved', 'paid')),
    FOREIGN KEY (teacher_id) REFERENCES core_teacher(id) ON DELETE CASCADE
);

-- Индексы для таблицы core_timesheet
CREATE INDEX IF NOT EXISTS idx_core_timesheet_teacher_id ON core_timesheet(teacher_id);
CREATE INDEX IF NOT EXISTS idx_core_timesheet_period ON core_timesheet(period);
CREATE INDEX IF NOT EXISTS idx_core_timesheet_status ON core_timesheet(status);

-- =====================================================
-- Таблица: core_salary (Salary)
-- Описание: Зарплаты преподавателей
-- =====================================================
CREATE TABLE IF NOT EXISTS core_salary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    period DATE NOT NULL,
    base_salary DECIMAL(10, 2) NOT NULL,
    bonus DECIMAL(10, 2) NOT NULL DEFAULT 0,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES core_teacher(id) ON DELETE CASCADE
);

-- Индексы для таблицы core_salary
CREATE INDEX IF NOT EXISTS idx_core_salary_teacher_id ON core_salary(teacher_id);
CREATE INDEX IF NOT EXISTS idx_core_salary_period ON core_salary(period);

-- =====================================================
-- Таблица: core_feedback (Feedback)
-- Описание: Обратная связь от пользователей
-- =====================================================
CREATE TABLE IF NOT EXISTS core_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subject VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'new' CHECK(status IN ('new', 'reviewed')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- Индексы для таблицы core_feedback
CREATE INDEX IF NOT EXISTS idx_core_feedback_user_id ON core_feedback(user_id);
CREATE INDEX IF NOT EXISTS idx_core_feedback_status ON core_feedback(status);
CREATE INDEX IF NOT EXISTS idx_core_feedback_created_at ON core_feedback(created_at);

-- =====================================================
-- Конец скрипта
-- =====================================================



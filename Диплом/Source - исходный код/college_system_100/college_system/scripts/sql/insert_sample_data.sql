-- =====================================================
-- SQL скрипт для вставки тестовых данных
-- База данных: SQLite
-- =====================================================

-- Включение поддержки внешних ключей
PRAGMA foreign_keys = ON;

-- =====================================================
-- Примеры данных для отчета
-- =====================================================

-- Вставка пользователей
INSERT INTO auth_user (username, email, password, role, is_staff, is_active, date_joined) VALUES
('admin', 'admin@college.ru', 'pbkdf2_sha256$...', 'admin', 1, 1, datetime('now')),
('accountant1', 'accountant@college.ru', 'pbkdf2_sha256$...', 'accountant', 1, 1, datetime('now')),
('teacher1', 'teacher1@college.ru', 'pbkdf2_sha256$...', 'teacher', 0, 1, datetime('now')),
('teacher2', 'teacher2@college.ru', 'pbkdf2_sha256$...', 'teacher', 0, 1, datetime('now')),
('curator1', 'curator@college.ru', 'pbkdf2_sha256$...', 'curator', 0, 1, datetime('now'));

-- Вставка преподавателей
INSERT INTO core_teacher (user_id, full_name, position, academic_degree, rate, is_active) VALUES
(3, 'Иванов Иван Иванович', 'Старший преподаватель', 'Кандидат наук', 1500.00, 1),
(4, 'Петрова Мария Сергеевна', 'Доцент', 'Доктор наук', 2000.00, 1);

-- Вставка предметов
INSERT INTO core_subject (name, code, description, is_active) VALUES
('Математика', 'MATH-101', 'Основы математического анализа', 1),
('Информатика', 'CS-201', 'Основы программирования', 1),
('Физика', 'PHYS-101', 'Общая физика', 1),
('Базы данных', 'DB-301', 'Проектирование и разработка БД', 1);

-- Вставка учебных групп
INSERT INTO core_studygroup (name, is_active) VALUES
('ИТ-21', 1),
('ИТ-22', 1),
('ИТ-31', 1),
('ИТ-32', 1);

-- Вставка учебной нагрузки
INSERT INTO core_workload (teacher_id, subject_id, group_id, date, activity_type, pair_slot, description) VALUES
(1, 1, 1, date('now'), 'lecture', '1', 'Лекция по математическому анализу'),
(1, 1, 1, date('now'), 'practice', '2', 'Практическое занятие'),
(1, 2, 2, date('now', '+1 day'), 'lab', '3', 'Лабораторная работа по программированию'),
(2, 4, 3, date('now'), 'lecture', '1', 'Лекция по базам данных'),
(2, 4, 3, date('now'), 'practice', '2', 'Практика по SQL');

-- Вставка табелей
INSERT INTO core_timesheet (teacher_id, period, total_hours, status) VALUES
(1, date('now', 'start of month'), 120.00, 'approved'),
(1, date('now', '-1 month', 'start of month'), 115.50, 'paid'),
(2, date('now', 'start of month'), 100.00, 'draft'),
(2, date('now', '-1 month', 'start of month'), 98.00, 'paid');

-- Вставка зарплат
INSERT INTO core_salary (teacher_id, period, base_salary, bonus, total_amount) VALUES
(1, date('now', '-1 month', 'start of month'), 180000.00, 5000.00, 185000.00),
(2, date('now', '-1 month', 'start of month'), 240000.00, 10000.00, 250000.00),
(1, date('now', '-2 months', 'start of month'), 180000.00, 0.00, 180000.00),
(2, date('now', '-2 months', 'start of month'), 240000.00, 5000.00, 245000.00);

-- Вставка обратной связи
INSERT INTO core_feedback (user_id, subject, message, status, created_at) VALUES
(3, 'Вопрос по расписанию', 'Когда будет следующая лекция?', 'reviewed', datetime('now', '-2 days')),
(4, 'Предложение', 'Можно ли добавить дополнительные материалы?', 'new', datetime('now', '-1 day')),
(5, 'Благодарность', 'Спасибо за интересные занятия!', 'reviewed', datetime('now', '-3 days'));

-- =====================================================
-- Конец скрипта
-- =====================================================



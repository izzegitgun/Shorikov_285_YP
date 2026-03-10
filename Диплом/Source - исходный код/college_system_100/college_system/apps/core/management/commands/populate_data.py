"""
Management command для заполнения базы данных тестовыми данными
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import random

from apps.core.models import Teacher, Subject, StudyGroup, Workload, Timesheet, Salary

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными (преподаватели, предметы, группы, нагрузка, табели, зарплата)'

    def handle(self, *args, **options):
        self.stdout.write('Начинаю заполнение базы данных...')
        
        # Создание пользователей и преподавателей
        teachers = self.create_teachers()
        self.stdout.write(self.style.SUCCESS(f'[OK] Создано {len(teachers)} преподавателей'))
        
        # Создание предметов
        subjects = self.create_subjects()
        self.stdout.write(self.style.SUCCESS(f'[OK] Создано {len(subjects)} предметов'))
        
        # Создание групп
        groups = self.create_groups()
        self.stdout.write(self.style.SUCCESS(f'[OK] Создано {len(groups)} групп'))
        
        # Создание нагрузки
        workloads = self.create_workloads(teachers, subjects, groups)
        self.stdout.write(self.style.SUCCESS(f'[OK] Создано {len(workloads)} записей нагрузки'))
        
        # Создание табелей
        timesheets = self.create_timesheets(teachers, subjects, groups)
        self.stdout.write(self.style.SUCCESS(f'[OK] Создано {len(timesheets)} табелей'))
        
        # Создание зарплат
        salaries = self.create_salaries(teachers)
        self.stdout.write(self.style.SUCCESS(f'[OK] Создано {len(salaries)} записей зарплаты'))
        
        total = len(teachers) + len(subjects) + len(groups) + len(workloads) + len(timesheets) + len(salaries)
        self.stdout.write(self.style.SUCCESS(f'\n[OK] Всего создано {total} записей'))

    def create_teachers(self):
        """Создает преподавателей"""
        teacher_data = [
            {'full_name': 'Смирнов Алексей Владимирович', 'position': 'Профессор', 'academic_degree': 'Доктор наук', 'rate': 2500.00},
            {'full_name': 'Козлова Елена Петровна', 'position': 'Доцент', 'academic_degree': 'Кандидат наук', 'rate': 2000.00},
            {'full_name': 'Волков Дмитрий Сергеевич', 'position': 'Старший преподаватель', 'academic_degree': 'Кандидат наук', 'rate': 1800.00},
            {'full_name': 'Новикова Анна Игоревна', 'position': 'Преподаватель', 'academic_degree': 'Магистр', 'rate': 1500.00},
            {'full_name': 'Морозов Игорь Александрович', 'position': 'Доцент', 'academic_degree': 'Доктор наук', 'rate': 2200.00},
            {'full_name': 'Лебедева Ольга Викторовна', 'position': 'Старший преподаватель', 'academic_degree': 'Кандидат наук', 'rate': 1700.00},
            {'full_name': 'Соколов Павел Николаевич', 'position': 'Профессор', 'academic_degree': 'Доктор наук', 'rate': 2400.00},
            {'full_name': 'Федорова Мария Дмитриевна', 'position': 'Преподаватель', 'academic_degree': 'Магистр', 'rate': 1600.00},
        ]
        
        teachers = []
        for i, data in enumerate(teacher_data, start=1):
            username = f'teacher{i+2}'  # Начинаем с teacher3, так как могут быть существующие
            email = f'teacher{i+2}@college.ru'
            
            # Проверяем, существует ли пользователь
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'role': User.Roles.TEACHER,
                    'is_active': True,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            
            # Создаем или получаем преподавателя
            teacher, created = Teacher.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': data['full_name'],
                    'position': data['position'],
                    'academic_degree': data['academic_degree'],
                    'rate': Decimal(str(data['rate'])),
                    'is_active': True,
                }
            )
            teachers.append(teacher)
        
        return teachers

    def create_subjects(self):
        """Создает предметы"""
        subjects_data = [
            {'name': 'Алгоритмы и структуры данных', 'code': 'CS-301', 'description': 'Изучение основных алгоритмов и структур данных'},
            {'name': 'Веб-разработка', 'code': 'WEB-201', 'description': 'Создание веб-приложений'},
            {'name': 'Машинное обучение', 'code': 'ML-401', 'description': 'Основы машинного обучения и нейронных сетей'},
            {'name': 'Компьютерные сети', 'code': 'NET-301', 'description': 'Протоколы и архитектура сетей'},
            {'name': 'Операционные системы', 'code': 'OS-201', 'description': 'Принципы работы операционных систем'},
            {'name': 'Кибербезопасность', 'code': 'SEC-401', 'description': 'Защита информации и систем'},
            {'name': 'Мобильная разработка', 'code': 'MOB-301', 'description': 'Разработка мобильных приложений'},
            {'name': 'Базы данных (продвинутый курс)', 'code': 'DB-401', 'description': 'Продвинутые техники работы с БД'},
        ]
        
        subjects = []
        for data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                name=data['name'],
                defaults={
                    'code': data['code'],
                    'description': data['description'],
                    'is_active': True,
                }
            )
            subjects.append(subject)
        
        return subjects

    def create_groups(self):
        """Создает учебные группы"""
        groups_data = [
            'ИТ-23',
            'ИТ-24',
            'ИТ-33',
            'ИТ-34',
            'ИТ-41',
            'ИТ-42',
            'ПМИ-21',
            'ПМИ-22',
        ]
        
        groups = []
        for name in groups_data:
            group, created = StudyGroup.objects.get_or_create(
                name=name,
                defaults={'is_active': True}
            )
            groups.append(group)
        
        return groups

    def create_workloads(self, teachers, subjects, groups):
        """Создает учебную нагрузку"""
        workloads = []
        activity_types = ['lecture', 'practice', 'lab']
        pair_slots = ['1', '2', '3', '4', '5', '6']
        
        # Создаем примерно 20 записей нагрузки
        for i in range(20):
            teacher = random.choice(teachers)
            subject = random.choice(subjects)
            group = random.choice(groups) if random.random() > 0.1 else None  # 10% без группы
            activity_type = random.choice(activity_types)
            pair_slot = random.choice(pair_slots)
            
            # Случайная дата в ближайшие 30 дней
            days_offset = random.randint(-15, 15)
            workload_date = date.today() + timedelta(days=days_offset)
            
            descriptions = {
                'lecture': f'Лекция по теме "{subject.name}"',
                'practice': f'Практическое занятие по "{subject.name}"',
                'lab': f'Лабораторная работа по "{subject.name}"',
            }
            
            workload = Workload.objects.create(
                teacher=teacher,
                subject=subject,
                group=group,
                date=workload_date,
                activity_type=activity_type,
                pair_slot=pair_slot,
                description=descriptions[activity_type],
            )
            workloads.append(workload)
        
        return workloads

    def create_timesheets(self, teachers, subjects, groups):
        """Создает табели"""
        timesheets = []
        statuses = ['draft', 'approved', 'paid']
        
        # Создаем примерно 20 табелей
        for i in range(20):
            teacher = random.choice(teachers)
            subject = random.choice(subjects) if random.random() > 0.2 else None  # 20% без предмета
            group = random.choice(groups) if random.random() > 0.3 else None  # 30% без группы
            status = random.choice(statuses)
            
            # Период - случайный месяц в последние 6 месяцев
            months_ago = random.randint(0, 5)
            period_from = date.today().replace(day=1) - timedelta(days=30 * months_ago)
            period_to = (period_from + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            # Случайные часы
            lecture_hours = Decimal(str(random.randint(0, 40)))
            practice_hours = Decimal(str(random.randint(0, 30)))
            lab_hours = Decimal(str(random.randint(0, 20)))
            
            timesheet = Timesheet.objects.create(
                teacher=teacher,
                subject=subject,
                group=group,
                period_from=period_from,
                period_to=period_to,
                period=period_from,  # Для обратной совместимости
                lecture_hours=lecture_hours,
                practice_hours=practice_hours,
                lab_hours=lab_hours,
                status=status,
            )
            timesheets.append(timesheet)
        
        return timesheets

    def create_salaries(self, teachers):
        """Создает записи о зарплате"""
        salaries = []
        
        # Создаем примерно 20 записей зарплаты
        for i in range(20):
            teacher = random.choice(teachers)
            
            # Период - случайный месяц в последние 6 месяцев
            months_ago = random.randint(0, 5)
            period = date.today().replace(day=1) - timedelta(days=30 * months_ago)
            
            # Проверяем, нет ли уже зарплаты за этот период для этого преподавателя
            if Salary.objects.filter(teacher=teacher, period=period).exists():
                continue
            
            # Базовая зарплата зависит от ставки преподавателя
            base_rate = float(teacher.rate)
            base_salary = Decimal(str(random.randint(int(base_rate * 80), int(base_rate * 120))))
            bonus = Decimal(str(random.randint(0, int(base_rate * 10))))
            total_amount = base_salary + bonus
            
            salary = Salary.objects.create(
                teacher=teacher,
                period=period,
                base_salary=base_salary,
                bonus=bonus,
                total_amount=total_amount,
            )
            salaries.append(salary)
        
        return salaries


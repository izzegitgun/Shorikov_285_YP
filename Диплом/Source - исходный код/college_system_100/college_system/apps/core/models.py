from django.conf import settings
from django.db import models


class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    academic_degree = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.full_name


class Subject(models.Model):
    """Учебные дисциплины/предметы."""

    name = models.CharField(max_length=150, verbose_name="Название предмета")
    code = models.CharField(max_length=50, blank=True, verbose_name="Код (по учебному плану)")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self) -> str:
        return self.name


class StudyGroup(models.Model):
    """Учебные группы."""

    name = models.CharField(max_length=100, unique=True, verbose_name="Название группы")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Workload(models.Model):
    ACTIVITY_CHOICES = [
        ("lecture", "Лекция"),
        ("practice", "Практика"),
        ("lab", "Лабораторная работа"),
    ]

    PAIR_CHOICES = [
        ("1", "1 пара (09:00–10:35)"),
        ("2", "2 пара (10:45–12:20)"),
        ("3", "3 пара (13:00–14:35)"),
        ("4", "4 пара (14:45–17:15)"),
        ("5", "5 пара (16:30–18:05)"),
        ("6", "6 пара (18:15–19:50)"),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="workloads")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="workloads")
    group = models.ForeignKey(
        StudyGroup,
        on_delete=models.CASCADE,
        related_name="workloads",
        null=True,
        blank=True,
    )
    date = models.DateField()
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    pair_slot = models.CharField(
        max_length=1,
        choices=PAIR_CHOICES,
        verbose_name="Пара",
        blank=True,
    )
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        pair = dict(self.PAIR_CHOICES).get(self.pair_slot, self.pair_slot or "—")
        group = self.group or "Без группы"
        return f"{self.teacher} {self.subject} {group} {self.date} {pair}"


class Timesheet(models.Model):
    STATUS_CHOICES = [
        ("draft", "Черновик"),
        ("approved", "Утвержден"),
        ("paid", "Оплачен"),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="timesheets", verbose_name="Преподаватель")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="timesheets", verbose_name="Дисциплина", null=True, blank=True)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name="timesheets", verbose_name="Группа", null=True, blank=True)
    period_from = models.DateField(verbose_name="Период с", null=True, blank=True)
    period_to = models.DateField(verbose_name="Период до", null=True, blank=True)
    lecture_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Часы за лекции")
    practice_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Часы за практику")
    lab_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Часы за лабораторные работы")
    total_hours = models.DecimalField(max_digits=8, decimal_places=2, editable=False, verbose_name="Итого")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft", verbose_name="Статус")
    
    # Сохраняем старое поле period для обратной совместимости (будет удалено в будущем)
    period = models.DateField(help_text="Первый день месяца", null=True, blank=True)

    class Meta:
        verbose_name = "Табель"
        verbose_name_plural = "Табели"
        ordering = ["-period_from"]

    def save(self, *args, **kwargs):
        # Автоматический подсчёт итого
        self.total_hours = (self.lecture_hours or 0) + (self.practice_hours or 0) + (self.lab_hours or 0)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Табель {self.teacher} - {self.subject} ({self.period_from:%d.%m.%Y} - {self.period_to:%d.%m.%Y})"


class Salary(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="salaries")
    period = models.DateField(help_text="Первый день месяца")
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"Зарплата {self.teacher} за {self.period:%m.%Y}"


class Feedback(models.Model):
    STATUS_NEW = "new"
    STATUS_REVIEWED = "reviewed"

    STATUS_CHOICES = [
        (STATUS_NEW, "Новый"),
        (STATUS_REVIEWED, "Просмотрено"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )
    subject = models.CharField(max_length=150)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Сообщение пользователя"
        verbose_name_plural = "Сообщения пользователей"

    def __str__(self) -> str:
        return f"{self.subject} от {self.user.username}"


class Message(models.Model):
    """Простые личные сообщения между кураторами и преподавателями."""

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )
    body = models.TextField(verbose_name="Сообщение")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.sender} → {self.recipient}: {self.body[:40]}"



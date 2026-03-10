from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Teacher",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=100)),
                ("position", models.CharField(max_length=100)),
                ("academic_degree", models.CharField(max_length=50)),
                ("rate", models.DecimalField(decimal_places=2, max_digits=10)),
                ("is_active", models.BooleanField(default=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="teacher_profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Timesheet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("period", models.DateField(help_text="Первый день месяца")),
                ("total_hours", models.DecimalField(decimal_places=2, max_digits=8)),
                ("status", models.CharField(choices=[("draft", "Черновик"), ("approved", "Утвержден"), ("paid", "Оплачен")], default="draft", max_length=20)),
                ("teacher", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="timesheets", to="core.teacher")),
            ],
        ),
        migrations.CreateModel(
            name="Workload",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("activity_type", models.CharField(choices=[("lecture", "Лекция"), ("seminar", "Семинар"), ("methodical", "Методическая работа")], max_length=50)),
                ("hours", models.DecimalField(decimal_places=2, max_digits=5)),
                ("description", models.TextField(blank=True)),
                ("teacher", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="workloads", to="core.teacher")),
            ],
        ),
        migrations.CreateModel(
            name="Salary",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("period", models.DateField(help_text="Первый день месяца")),
                ("base_salary", models.DecimalField(decimal_places=2, max_digits=10)),
                ("bonus", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("teacher", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="salaries", to="core.teacher")),
            ],
        ),
    ]



from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="Название предмета")),
                ("code", models.CharField(blank=True, max_length=50, verbose_name="Код (по учебному плану)")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активен")),
            ],
            options={
                "verbose_name": "Предмет",
                "verbose_name_plural": "Предметы",
            },
        ),
        migrations.AlterField(
            model_name="workload",
            name="activity_type",
            field=models.CharField(
                choices=[
                    ("lecture", "Лекция"),
                    ("practice", "Практика"),
                    ("lab", "Лабораторная работа"),
                ],
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="workload",
            name="subject",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="workloads",
                to="core.subject",
            ),
            preserve_default=False,
        ),
    ]



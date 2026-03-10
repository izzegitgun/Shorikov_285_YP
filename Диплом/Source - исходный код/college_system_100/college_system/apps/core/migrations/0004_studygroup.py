from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_feedback"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudyGroup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="Название группы")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активна")),
            ],
            options={
                "verbose_name": "Группа",
                "verbose_name_plural": "Группы",
                "ordering": ["name"],
            },
        ),
    ]




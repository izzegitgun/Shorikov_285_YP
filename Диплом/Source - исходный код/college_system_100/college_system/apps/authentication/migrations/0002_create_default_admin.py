from django.db import migrations


def create_default_admin(apps, schema_editor):
    User = apps.get_model("authentication", "User")
    if not User.objects.filter(username="Shorikov").exists():
        User.objects.create_superuser(
            username="Shorikov",
            email="admin@kpsu.local",
            password="kpsu!KPSU",
            role="admin",
            first_name="Антон",
            last_name="Шориков",
        )


def remove_default_admin(apps, schema_editor):
    User = apps.get_model("authentication", "User")
    User.objects.filter(username="Shorikov").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_admin, remove_default_admin),
    ]



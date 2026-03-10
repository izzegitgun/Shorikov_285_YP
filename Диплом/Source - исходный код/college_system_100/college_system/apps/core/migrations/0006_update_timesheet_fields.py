# Generated manually for Timesheet model updates

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_workload_hours_workload_group_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='subject',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='timesheets', to='core.subject', verbose_name='Дисциплина'),
        ),
        migrations.AddField(
            model_name='timesheet',
            name='group',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='timesheets', to='core.studygroup', verbose_name='Группа'),
        ),
        migrations.AddField(
            model_name='timesheet',
            name='period_from',
            field=models.DateField(null=True, blank=True, verbose_name='Период с'),
        ),
        migrations.AddField(
            model_name='timesheet',
            name='period_to',
            field=models.DateField(null=True, blank=True, verbose_name='Период до'),
        ),
        migrations.AddField(
            model_name='timesheet',
            name='lecture_hours',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Часы за лекции'),
        ),
        migrations.AddField(
            model_name='timesheet',
            name='practice_hours',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Часы за практику'),
        ),
        migrations.AddField(
            model_name='timesheet',
            name='lab_hours',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Часы за лабораторные работы'),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='period',
            field=models.DateField(blank=True, help_text='Первый день месяца', null=True),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='total_hours',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=8, verbose_name='Итого'),
        ),
    ]


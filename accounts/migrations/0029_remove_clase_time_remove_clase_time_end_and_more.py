# Generated by Django 4.0 on 2024-04-25 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_alter_horario_day_of_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clase',
            name='time',
        ),
        migrations.RemoveField(
            model_name='clase',
            name='time_end',
        ),
        migrations.AddField(
            model_name='horario',
            name='time_end',
            field=models.TimeField(null=True),
        ),
    ]
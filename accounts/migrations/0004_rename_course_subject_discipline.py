# Generated by Django 4.0 on 2024-05-08 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_teacher_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='course',
            new_name='discipline',
        ),
    ]

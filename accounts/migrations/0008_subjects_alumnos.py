# Generated by Django 4.0 on 2024-03-29 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_user_user_type_alter_subjects_staff_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjects',
            name='alumnos',
            field=models.ManyToManyField(to='accounts.Students'),
        ),
    ]
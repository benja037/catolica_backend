# Generated by Django 4.0 on 2024-04-04 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_remove_students_address_remove_teachers_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.user'),
        ),
    ]

# Generated by Django 4.0 on 2024-05-23 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_student_document_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentClassRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.CharField(default='pendiente', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('class_instance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.classinstance')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
    ]

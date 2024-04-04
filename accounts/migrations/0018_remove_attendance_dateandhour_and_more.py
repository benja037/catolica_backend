# Generated by Django 4.0 on 2024-04-04 19:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_students_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='dateandhour',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='subject_id',
        ),
        migrations.AddField(
            model_name='attendance',
            name='user_estado_previo',
            field=models.CharField(choices=[('asistire', 'Asistiré'), ('no-asistire', 'no-asistire'), ('no-responde', 'No responde')], default='no-responde', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='student_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.students'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='courses',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('hombre', 'hombre'), ('mujer', 'mujer')], max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_and_hour', models.DateTimeField()),
                ('estado', models.CharField(choices=[('proximamente', 'proximamente'), ('realizada', 'realizada'), ('realizada-parcial', 'realizada-parcial'), ('cancelada', 'cancelada')], default='proximamente', max_length=255)),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.subjects')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='clase_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.clase'),
        ),
    ]

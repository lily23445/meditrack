# Generated by Django 5.1.4 on 2025-03-13 14:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo_app', '0009_remove_medicinelog_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicineStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('taken', 'Taken'), ('missed', 'Missed')], max_length=10)),
                ('medicine_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo_app.medicinelog')),
            ],
        ),
    ]

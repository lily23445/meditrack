# Generated by Django 5.1.4 on 2025-03-13 09:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo_app', '0003_uploadedfile_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicineLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('time', models.CharField(choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('night', 'Night')], max_length=50)),
                ('status', models.CharField(choices=[('taken', 'Taken'), ('missed', 'Missed')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

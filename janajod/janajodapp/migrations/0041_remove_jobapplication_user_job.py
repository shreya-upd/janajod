# Generated by Django 4.1.13 on 2024-11-13 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('janajodapp', '0040_jobapplication_user_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobapplication',
            name='user_job',
        ),
    ]

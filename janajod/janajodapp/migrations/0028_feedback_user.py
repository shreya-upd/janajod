# Generated by Django 4.1.13 on 2024-10-22 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('janajodapp', '0027_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

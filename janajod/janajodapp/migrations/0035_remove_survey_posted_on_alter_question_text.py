# Generated by Django 4.1.13 on 2024-10-26 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('janajodapp', '0034_survey_question_option'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='posted_on',
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=200),
        ),
    ]

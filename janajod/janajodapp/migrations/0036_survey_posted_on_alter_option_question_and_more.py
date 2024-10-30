# Generated by Django 4.1.13 on 2024-10-26 07:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('janajodapp', '0035_remove_survey_posted_on_alter_question_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='posted_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='option',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='janajodapp.question'),
        ),
        migrations.AlterField(
            model_name='option',
            name='text',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='janajodapp.survey'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='survey',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
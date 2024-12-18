# Generated by Django 4.1.13 on 2024-10-30 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('janajodapp', '0038_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitteeMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('contribution', models.TextField()),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='images/users/')),
            ],
        ),
    ]

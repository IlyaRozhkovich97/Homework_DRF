# Generated by Django 5.0.7 on 2024-07-22 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_alter_lesson_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='lesson_url',
            field=models.URLField(blank=True, null=True, verbose_name='ссылка на видео'),
        ),
    ]
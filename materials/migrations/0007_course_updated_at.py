# Generated by Django 5.0.7 on 2024-07-31 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0006_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='обновлено'),
        ),
    ]

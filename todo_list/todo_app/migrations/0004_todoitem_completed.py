# Generated by Django 3.2.9 on 2023-11-19 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0003_remove_todoitem_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]

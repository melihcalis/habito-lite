# Generated by Django 4.2.5 on 2023-10-01 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='streak',
        ),
    ]
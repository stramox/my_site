# Generated by Django 5.0.9 on 2024-11-27 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
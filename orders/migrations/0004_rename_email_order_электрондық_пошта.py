# Generated by Django 4.2.16 on 2024-12-01 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20210904_1200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='email',
            new_name='электрондық_пошта',
        ),
    ]

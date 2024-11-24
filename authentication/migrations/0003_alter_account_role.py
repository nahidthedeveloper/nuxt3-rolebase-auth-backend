# Generated by Django 4.2 on 2024-11-24 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_account_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], max_length=150),
        ),
    ]

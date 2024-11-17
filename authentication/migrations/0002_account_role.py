# Generated by Django 4.2 on 2024-11-09 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User'), ('manager', 'Manager')], default=2, max_length=150),
            preserve_default=False,
        ),
    ]

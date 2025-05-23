# Generated by Django 5.2 on 2025-04-24 05:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0009_server_author_server_created_server_extra_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='cpu',
            field=models.IntegerField(blank=True, help_text='Cores', null=True, validators=[django.core.validators.MaxValueValidator(16)]),
        ),
        migrations.AlterField(
            model_name='server',
            name='disk',
            field=models.IntegerField(blank=True, help_text='Disk GB', null=True, validators=[django.core.validators.MaxValueValidator(65536)]),
        ),
        migrations.AlterField(
            model_name='server',
            name='memory',
            field=models.IntegerField(blank=True, help_text='RAM GB', null=True, validators=[django.core.validators.MaxValueValidator(65536)]),
        ),
    ]

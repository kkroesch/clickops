# Generated by Django 5.0.6 on 2024-06-21 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("servers", "0003_network_remove_server_primary_ip_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="server",
            name="name",
            field=models.CharField(max_length=200),
        ),
    ]

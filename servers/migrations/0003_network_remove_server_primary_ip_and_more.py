# Generated by Django 4.2.11 on 2024-06-21 13:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("servers", "0002_server_network_alter_server_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Network",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vlan_name", models.CharField(max_length=100)),
                ("ipv4_address", models.GenericIPAddressField(protocol="IPv4")),
                (
                    "netmask",
                    models.GenericIPAddressField(
                        default="255.255.255.0", protocol="IPv4"
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="server",
            name="primary_ip",
        ),
        migrations.AddField(
            model_name="server",
            name="primary_ip_address",
            field=models.GenericIPAddressField(null=True, protocol="IPv4", unique=True),
        ),
        migrations.AlterField(
            model_name="server",
            name="cpu",
            field=models.IntegerField(
                default=2, validators=[django.core.validators.MaxValueValidator(16)]
            ),
        ),
        migrations.AlterField(
            model_name="server",
            name="disk",
            field=models.IntegerField(
                default=32, validators=[django.core.validators.MaxValueValidator(65536)]
            ),
        ),
        migrations.AlterField(
            model_name="server",
            name="memory",
            field=models.IntegerField(
                default=1024,
                validators=[django.core.validators.MaxValueValidator(65536)],
            ),
        ),
        migrations.AlterField(
            model_name="server",
            name="name",
            field=models.CharField(default="srv08118873", max_length=200),
        ),
        migrations.AlterField(
            model_name="server",
            name="network",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="servers",
                to="servers.network",
            ),
        ),
    ]

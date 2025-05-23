# Generated by Django 5.0.6 on 2024-06-22 06:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("servers", "0005_operatingsystem_alter_server_name_alter_server_os"),
    ]

    operations = [
        migrations.CreateModel(
            name="Domain",
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
                ("name", models.CharField(max_length=200)),
                ("ns1", models.CharField(max_length=200)),
                ("ns2", models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name="server",
            name="status",
            field=models.CharField(
                choices=[
                    ("PEN", "Pending"),
                    ("ACT", "Active"),
                    ("APP", "Approved"),
                    ("REJ", "Rejected"),
                    ("DEL", "Deleted"),
                ],
                default="PEN",
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="server",
            name="domain",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="servers",
                to="servers.domain",
            ),
        ),
    ]

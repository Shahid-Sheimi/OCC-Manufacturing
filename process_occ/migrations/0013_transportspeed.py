# Generated by Django 4.1 on 2024-05-04 20:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0012_transportmode"),
    ]

    operations = [
        migrations.CreateModel(
            name="TransportSpeed",
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
                (
                    "transport_speed",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
            ],
        ),
    ]

# Generated by Django 4.1 on 2024-05-04 20:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0011_remove_kgco2epertxkm_transport_mode_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TransportMode",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
    ]

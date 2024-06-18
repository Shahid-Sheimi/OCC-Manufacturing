# Generated by Django 4.1 on 2024-05-04 20:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0016_kgco2epertxkm"),
    ]

    operations = [
        migrations.CreateModel(
            name="PackagingMaterial",
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
                ("name", models.CharField(max_length=20)),
                ("m2", models.FloatField(default=0, null=True)),
                ("weight_per_m2", models.FloatField(default=0, null=True)),
                ("kgCO2_per_kg", models.FloatField(default=0, null=True)),
            ],
        ),
    ]

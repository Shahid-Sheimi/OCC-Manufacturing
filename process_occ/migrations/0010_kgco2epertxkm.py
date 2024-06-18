# Generated by Django 4.1 on 2024-05-04 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0009_packagingmaterial_transportmode_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="KgCo2ePerTxKm",
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
                ("kgCO2e_per_txkm", models.FloatField(blank=True, null=True)),
                (
                    "transport_mode",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="process_occ.transportmode",
                    ),
                ),
            ],
        ),
    ]
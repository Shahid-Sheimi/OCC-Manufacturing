# Generated by Django 4.1 on 2024-05-12 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("payments", "0003_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Shipping",
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
                    "tracking_no",
                    models.CharField(blank=True, max_length=25, null=True, unique=True),
                ),
                ("services", models.CharField(blank=True, max_length=20, null=True)),
                ("weight", models.FloatField(blank=True, null=True)),
                ("date", models.DateTimeField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Processing", "Processing"),
                            ("On_The_Way", "On_The_Way"),
                            ("Arrived", "Arrived"),
                        ],
                        max_length=25,
                        null=True,
                    ),
                ),
                (
                    "transaction",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="payments.transaction",
                    ),
                ),
            ],
        ),
    ]

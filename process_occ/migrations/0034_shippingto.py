# Generated by Django 4.1 on 2024-05-09 19:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "process_occ",
            "0033_remove_tolerance_material_product_co2_intensity_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="ShippingTo",
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
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("company", models.CharField(blank=True, max_length=100, null=True)),
                ("address", models.CharField(blank=True, max_length=100, null=True)),
                ("city_town", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "state_region_province",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("zip_postal_pinconde", models.IntegerField(blank=True, null=True)),
                ("country", models.CharField(blank=True, max_length=50, null=True)),
                ("phone_number", models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]

# Generated by Django 4.1 on 2024-05-08 16:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0031_remove_product_country_co2_intensity"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="carbon_footprint_CO2",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
# Generated by Django 4.1 on 2024-05-14 23:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0043_quote_transaction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="carbon_footprint_CO2",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
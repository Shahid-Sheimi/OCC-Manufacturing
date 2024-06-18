# Generated by Django 4.1 on 2024-05-05 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0021_rename_kgco2epertxkm_kgco2epertonkm"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="kg_CO2e_packaging",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="total_packaging_weight",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name="order",
            name="products",
        ),
        migrations.AddField(
            model_name="order",
            name="products",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="process_occ.product",
            ),
        ),
    ]

# Generated by Django 4.1 on 2024-05-01 14:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0003_material_density_product_material_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="Material_id",
            new_name="material",
        ),
        migrations.AddField(
            model_name="coatings",
            name="mega_joules_per_mm_sqaure",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="heattreatment",
            name="mega_joules_per_kg",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="inspections",
            name="kilowatt_hours_per_mm_sqaure",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="material",
            name="kilo_gram_carbon_dioxide_equivalent_per_kg",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="material",
            name="mega_joules_per_kg",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="billet_volume",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="billet_weight",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="height_extend_percentage",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="product",
            name="length_extend_percentage",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="product",
            name="width_extend_percentage",
            field=models.FloatField(default=0),
        ),
    ]

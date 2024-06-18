# Generated by Django 4.1 on 2024-05-02 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "process_occ",
            "0006_rename_mm2_coeff_cn_finished_material_mm2_coeff_cn_finished_price_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="heattreatment",
            name="cost_cn_per_kg",
        ),
        migrations.RemoveField(
            model_name="heattreatment",
            name="cost_eu_per_kg",
        ),
        migrations.RemoveField(
            model_name="heattreatment",
            name="cost_uk_per_kg",
        ),
        migrations.RemoveField(
            model_name="material",
            name="quantity",
        ),
        migrations.AddField(
            model_name="heattreatment",
            name="Country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.countryco2intensity",
            ),
        ),
        migrations.AddField(
            model_name="heattreatment",
            name="cost",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="coating",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.coatings",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.countryco2intensity",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="heat_treatment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.heattreatment",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="inspection",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.inspections",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="kg_CO2e_coating",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="kg_CO2e_inspection",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="kg_CO2e_machining",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="kg_CO2e_material",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="kg_CO2e_treatment",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="quantity",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="material",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.material",
            ),
        ),
        migrations.CreateModel(
            name="Tolerance",
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
                ("tolerance", models.FloatField(default=0)),
                (
                    "material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="process_occ.material",
                    ),
                ),
            ],
        ),
    ]
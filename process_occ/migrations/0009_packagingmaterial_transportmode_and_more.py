# Generated by Django 4.1 on 2024-05-04 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "process_occ",
            "0008_country_remove_countryco2intensity_country_name_and_more",
        ),
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
                ("weight_per_m2", models.FloatField(default=0)),
                ("kgCO2_per_kg", models.FloatField(default=0)),
                ("m2", models.FloatField(default=0)),
            ],
        ),
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
        migrations.RenameField(
            model_name="heattreatment",
            old_name="cost",
            new_name="cost_per_kg",
        ),
        migrations.RenameField(
            model_name="material",
            old_name="mm2_coeff_cn_finished_price",
            new_name="cost_per_kg",
        ),
        migrations.RemoveField(
            model_name="coatings",
            name="cost_cn_per_mm2",
        ),
        migrations.RemoveField(
            model_name="coatings",
            name="cost_eu_per_mm2",
        ),
        migrations.RemoveField(
            model_name="coatings",
            name="cost_uk_per_mm2",
        ),
        migrations.RemoveField(
            model_name="heattreatment",
            name="Country",
        ),
        migrations.RemoveField(
            model_name="inspections",
            name="cost_cn_per_mm2",
        ),
        migrations.RemoveField(
            model_name="inspections",
            name="cost_eu_per_mm2",
        ),
        migrations.RemoveField(
            model_name="inspections",
            name="cost_uk_per_mm2",
        ),
        migrations.RemoveField(
            model_name="material",
            name="mm2_coeff_eu_finished_price",
        ),
        migrations.RemoveField(
            model_name="material",
            name="mm2_coeff_uk_finished_price",
        ),
        migrations.RemoveField(
            model_name="material",
            name="mm3_coeff_cn_removed_price",
        ),
        migrations.RemoveField(
            model_name="material",
            name="mm3_coeff_eu_removed_price",
        ),
        migrations.RemoveField(
            model_name="material",
            name="mm3_coeff_uk_removed_price",
        ),
        migrations.AddField(
            model_name="coatings",
            name="cost_per_mm2",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="coatings",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.country",
            ),
        ),
        migrations.AddField(
            model_name="inspections",
            name="cost_per_mm2",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="inspections",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.country",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="billet_mm3",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="cost_coating",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="cost_heat_treatment",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="cost_inspection",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="cost_machining",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="cost_material",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="country_CO2_intensity",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.countryco2intensity",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="finished_mm2",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="finished_mm3",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="machining_mm2_coeff_finished_price",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="machining_mm3_coeff_removed_price",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="countryco2intensity",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.country",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.country",
            ),
        ),
        migrations.CreateModel(
            name="Transport",
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
                    "speed",
                    models.CharField(
                        choices=[
                            ("slow", "Slow"),
                            ("medium", "Medium"),
                            ("fast", "Fast"),
                        ],
                        max_length=10,
                    ),
                ),
                ("cost", models.IntegerField()),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="process_occ.country",
                    ),
                ),
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
        migrations.CreateModel(
            name="MaterialMM3RemovedPrice",
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
                ("mm3_coeff_removed_price", models.FloatField(blank=True, null=True)),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="process_occ.country",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MaterialMM2FinishedPrice",
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
                ("mm2_coeff_finished_price", models.FloatField(blank=True, null=True)),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="process_occ.country",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="heattreatment",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.country",
            ),
        ),
        migrations.AddField(
            model_name="material",
            name="machining_mm2_coeff_finished_price",
            field=models.ManyToManyField(to="process_occ.materialmm2finishedprice"),
        ),
        migrations.AddField(
            model_name="material",
            name="machining_mm3_coeff_removed_price",
            field=models.ManyToManyField(to="process_occ.materialmm3removedprice"),
        ),
    ]

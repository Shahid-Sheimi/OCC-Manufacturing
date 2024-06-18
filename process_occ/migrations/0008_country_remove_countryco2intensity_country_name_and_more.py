# Generated by Django 4.1 on 2024-05-02 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0007_remove_heattreatment_cost_cn_per_kg_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Country",
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
                ("name", models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="countryco2intensity",
            name="country_name",
        ),
        migrations.AddField(
            model_name="countryco2intensity",
            name="country",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.country",
            ),
            preserve_default=False,
        ),
    ]

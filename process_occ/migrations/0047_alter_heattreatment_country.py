# Generated by Django 4.1 on 2024-05-20 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "process_occ",
            "0046_alter_coatings_cost_per_mm2_alter_coatings_country_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="heattreatment",
            name="country",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="process_occ.country"
            ),
        ),
    ]
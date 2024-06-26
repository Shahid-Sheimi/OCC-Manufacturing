# Generated by Django 4.1 on 2024-05-20 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0046_alter_coatings_cost_per_mm2_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coatings",
            name="country",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.country",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="heattreatment",
            name="country",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.country",
            ),
            preserve_default=False,
        ),
    ]

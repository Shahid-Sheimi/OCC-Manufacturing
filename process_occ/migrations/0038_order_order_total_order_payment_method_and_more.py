# Generated by Django 4.1 on 2024-05-12 21:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0037_manufacturerlead_quote_termsandconditions_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_total",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_method",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="material",
            name="cost_per_kg",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="material",
            name="density",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="material",
            name="kilo_gram_carbon_dioxide_equivalent_per_kg",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="material",
            name="mega_joules_per_kg",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="material",
            name="price",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]

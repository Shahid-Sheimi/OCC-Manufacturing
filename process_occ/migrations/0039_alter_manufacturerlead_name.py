# Generated by Django 4.1 on 2024-05-12 23:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0038_order_order_total_order_payment_method_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="manufacturerlead",
            name="name",
            field=models.CharField(
                choices=[
                    ("express", "Express"),
                    ("fast", "Fast"),
                    ("normal", "Normal"),
                ],
                default="normal",
                max_length=25,
            ),
        ),
    ]

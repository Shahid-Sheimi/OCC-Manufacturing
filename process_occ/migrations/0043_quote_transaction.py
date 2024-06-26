# Generated by Django 4.1 on 2024-05-14 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0004_alter_transaction_txn_id"),
        ("process_occ", "0042_quote_delivery_charges_quote_tax"),
    ]

    operations = [
        migrations.AddField(
            model_name="quote",
            name="transaction",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="payments.transaction",
            ),
        ),
    ]

# Generated by Django 4.2.11 on 2024-04-19 19:50

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                ("company", models.CharField(blank=True, max_length=100)),
                ("address", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                (
                    "country",
                    models.CharField(
                        choices=[
                            ("US", "United States"),
                            ("UK", "United Kingdom"),
                            ("CA", "Canada"),
                        ],
                        max_length=2,
                    ),
                ),
                ("postal_code", models.CharField(max_length=20)),
                ("phone_number", models.CharField(max_length=20)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("DebitCard", "Debit Card"),
                            ("CreditCard", "Credit Card"),
                            ("Stripe", "Stripe"),
                            ("Paypal", "Paypal"),
                        ],
                        max_length=20,
                    ),
                ),
                ("card_holder_name", models.CharField(blank=True, max_length=100)),
                ("card_number", models.CharField(blank=True, max_length=16)),
                ("expiry_date", models.DateField(blank=True, null=True)),
                ("cvc", models.CharField(blank=True, max_length=4)),
                ("review", models.TextField(blank=True)),
                (
                    "ship_to",
                    models.CharField(
                        choices=[
                            ("Home", "Home"),
                            ("Work", "Work"),
                            ("Other", "Other"),
                        ],
                        max_length=10,
                    ),
                ),
            ],
        ),
    ]

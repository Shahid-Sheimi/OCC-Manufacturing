# Generated by Django 4.1 on 2024-05-12 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0039_alter_manufacturerlead_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="manufacturer",
            name="country",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.country",
            ),
        ),
    ]

# Generated by Django 4.1 on 2024-05-07 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("process_occ", "0023_parentmaterial_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="manufacturer",
            name="name",
        ),
        migrations.AddField(
            model_name="manufacturer",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="process_occ.country",
            ),
        ),
    ]

# Generated by Django 5.0.1 on 2024-01-13 17:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="last_borrowed_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="book",
            name="last_borrower",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="last_borrower",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="borrowed_by",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

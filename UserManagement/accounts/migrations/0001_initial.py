# Generated by Django 4.2.3 on 2023-12-20 02:46

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                (
                    "identity_id",
                    models.IntegerField(blank=True, null=True, unique=True),
                ),
                ("full_name", models.CharField(blank=True, max_length=150)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="InstructorRate",
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
                (
                    "rate",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=3,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.00")),
                            django.core.validators.MaxValueValidator(Decimal("5.00")),
                        ],
                    ),
                ),
                ("review", models.CharField(blank=True, max_length=1000, null=True)),
                (
                    "rate_date_created",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="ratings",
                        to="accounts.userprofile",
                    ),
                ),
            ],
        ),
    ]

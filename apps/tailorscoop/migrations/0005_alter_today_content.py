# Generated by Django 4.2.1 on 2023-09-18 03:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tailorscoop", "0004_clicklog"),
    ]

    operations = [
        migrations.AlterField(
            model_name="today",
            name="content",
            field=models.TextField(),
        ),
    ]

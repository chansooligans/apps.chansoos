# Generated by Django 4.2.1 on 2023-09-18 03:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("themind", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="randomnumber",
            old_name="value",
            new_name="value1",
        ),
        migrations.AddField(
            model_name="randomnumber",
            name="value2",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

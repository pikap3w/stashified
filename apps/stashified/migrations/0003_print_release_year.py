# Generated by Django 2.1.2 on 2018-10-25 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stashified', '0002_auto_20181025_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='print',
            name='release_year',
            field=models.DateField(blank=True, null=True),
        ),
    ]
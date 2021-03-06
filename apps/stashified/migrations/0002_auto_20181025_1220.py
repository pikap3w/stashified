# Generated by Django 2.1.2 on 2018-10-25 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stashified', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='haves',
            field=models.ManyToManyField(related_name='owned_by', to='stashified.Bag'),
        ),
        migrations.AlterField(
            model_name='user',
            name='wants',
            field=models.ManyToManyField(related_name='wanted_by', to='stashified.Bag'),
        ),
    ]

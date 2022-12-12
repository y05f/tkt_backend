# Generated by Django 4.1.4 on 2022-12-08 01:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entreprises', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entreprise',
            name='siren',
            field=models.CharField(max_length=9, unique=True, validators=[django.core.validators.RegexValidator('^/[0-9]{9}$')]),
        ),
        migrations.AlterField(
            model_name='result',
            name='year',
            field=models.PositiveIntegerField(),
        ),
    ]

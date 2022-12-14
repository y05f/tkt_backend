# Generated by Django 4.1.4 on 2022-12-08 02:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entreprises', '0003_alter_entreprise_siren'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entreprise',
            name='siren',
            field=models.CharField(max_length=9, unique=True, validators=[django.core.validators.RegexValidator('^/d{9}$', message='SIREN must be 9 digits')]),
        ),
    ]

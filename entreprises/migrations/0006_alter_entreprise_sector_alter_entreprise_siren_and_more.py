# Generated by Django 4.1.4 on 2022-12-08 02:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entreprises', '0005_alter_entreprise_siren'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entreprise',
            name='sector',
            field=models.CharField(choices=[('SE', 'Services'), ('EL', 'Electronic'), ('EN', 'Energy'), ('LU', 'Luxury'), ('RE', 'Retail'), ('OT', 'Other')], default='OT', help_text='Choice (Services, Electronic, Energy, Luxury, Retail or Other)', max_length=2),
        ),
        migrations.AlterField(
            model_name='entreprise',
            name='siren',
            field=models.CharField(help_text='a unique number of digits', max_length=9, unique=True, validators=[django.core.validators.RegexValidator('^\\d{9}$', message='SIREN must be 9 digits')]),
        ),
        migrations.AlterField(
            model_name='result',
            name='ca',
            field=models.PositiveIntegerField(help_text='Capital'),
        ),
    ]

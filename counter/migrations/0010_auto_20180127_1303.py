# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-01-27 18:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0009_auto_20180120_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='units',
            field=models.CharField(choices=[('grams', 'Grams'), ('ounces', 'Ounces'), ('kilograms', 'KIlograms'), ('pounds', 'Pounds'), ('milliliters', 'Milliliters'), ('Liters', 'Liters'), ('cup', 'Cup'), ('scoop', 'Scoop'), ('piece', 'Piece'), ('can', 'Can')], default='grams', max_length=15),
        ),
    ]
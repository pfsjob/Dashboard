# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-09 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creador', '0005_tareas_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tareas',
            name='estado',
            field=models.BooleanField(default=False),
        ),
    ]

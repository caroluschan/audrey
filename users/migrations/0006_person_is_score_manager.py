# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-18 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180316_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_score_manager',
            field=models.NullBooleanField(),
        ),
    ]

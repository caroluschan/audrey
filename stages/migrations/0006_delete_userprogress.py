# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-15 15:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stages', '0005_delete_stages'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProgress',
        ),
    ]
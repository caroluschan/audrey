# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Scores(models.Model):
	identifier = models.CharField(max_length=200)
	file_path = models.CharField(max_length=200)
	index = models.CharField(max_length=200)

class Index(models.Model):
	identifier = models.CharField(max_length=200)
	index = models.CharField(max_length=200)
	language = models.CharField(max_length=200, null=True, blank=True) #en, cn, others
	stroke = models.CharField(max_length=200, null=True, blank=True)
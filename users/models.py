# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from stages.models import *
from django.conf import settings
import telepot
import sys
import re

# Create your models here.

class Person(models.Model):
	telegram_id = models.CharField(max_length=200)
	user_name = models.CharField(max_length=200, null=True, blank=True)
	is_admin = models.NullBooleanField()
	is_approved = models.NullBooleanField()
	stage_code = models.CharField(max_length=200, null=True, blank=True)

	bot = telepot.Bot(settings.BOT_TOKEN)
	
	#####################
	####Stage Control####
	#####################

	def updateUserProgress(self, stage_code):		
		self.stage_code = stage_code
		self.save()

	def stageUp(self):
		pattern = re.compile('_')
		cutter = pattern.search(self.stage_code).span()[1]
		self.stage_code = self.stage_code[:cutter-len(self.stage_code)] + str(int(self.stage_code[cutter-len(self.stage_code):])+1)
		self.save()

	def stageDown(self):
		pattern = re.compile('_')
		cutter = pattern.search(self.stage_code).span()[1]
		self.stage_code = self.stage_code[:cutter-len(self.stage_code)] + str(int(self.stage_code[cutter-len(self.stage_code):])-1)
		self.save()

	def stageEnd(self):
		self.stage_code = None
		self.save()

	###################
	####User Config####
	###################

	def approve(self):
		self.is_approved = True
		self.save()

	def setName(self, name):
		self.user_name = name
		self.save()

	def setAsAdmin(self):
		self.is_admin = True
		self.save()

	def unsetAsAdmin(self):
		self.is_admin = False
		self.save()
	
	#######################
	####Outward Message####
	#######################

	def sendText(self, message):
		self.bot.sendMessage(self.telegram_id, message)

	def sendDocument(self, document, message=None):
		print('send doc')
		self.bot.sendDocument(self.telegram_id, open(document), message)

	def sendAudio(self, audio, message=None):
		print('send audio')
		self.bot.sendAudio(self, open(audio), message)
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from stages.models import *
from django.conf import settings
import telepot
import json
import sys
import re
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

# Create your models here.

class Person(models.Model):
	telegram_id = models.CharField(max_length=200)
	user_name = models.CharField(max_length=200, null=True, blank=True)
	is_admin = models.NullBooleanField()
	is_approved = models.NullBooleanField()
	is_score_manager = models.BooleanField(default=False)
	stage_code = models.CharField(max_length=200, null=True, blank=True)
	lang = models.CharField(max_length=200, default='cn')
	storage = models.CharField(max_length=200, null=True, blank=True)

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

	def getStageCode(self):
		pattern = re.compile('_')
		cutter = pattern.search(self.stage_code).span()[1]
		return self.stage_code[:cutter-len(self.stage_code)-1]

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

	def setAsScoreManager(self):
		self.is_score_manager = True
		self.save()

	def unsetAsScoreManager(self):
		self.is_score_manager = False
		self.save()

	def storageToJson(self):
		tmp = {}
		if self.storage is not None:
			tmp =json.loads(self.storage)
		return tmp

	def setStorage(self, key, value):
		tmp = self.storageToJson()
		tmp[key] = value
		self.storage = json.dumps(tmp)
		self.save()

	def popStorage(self, key):
		tmp = self.storageToJson()
		tmp.pop(key)
		self.storage = json.dumps(tmp)
		self.save()

	def getStorage(self, key=None):		
		return self.storageToJson()[key] if key is not None else self.storageToJson()

	def setLang(self, lang):
		self.lang = lang
		self.save()


	#######################
	####Outward Message####
	#######################

	def sendText(self, message, keyboard_content=[], with_cancel=True):
		function = []
		function.extend(keyboard_content)
		if with_cancel:
			function.append([InlineKeyboardButton(text='Cancel', callback_data='/cancel')]) 
		if len(function) > 0:
			keyboard = InlineKeyboardMarkup(inline_keyboard=function)
			self.bot.sendMessage(self.telegram_id, message, reply_markup=keyboard)
		else:
			self.bot.sendMessage(self.telegram_id, message)

	def sendDocument(self, document, message=None):
		print('send doc')
		self.bot.sendDocument(self.telegram_id, open(document), message)

	def sendAudio(self, audio, message=None):
		print('send audio')
		self.bot.sendAudio(self, open(audio), message)
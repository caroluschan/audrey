# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from stages.models import *
from users.models import *
from stages.assist import *
from django.conf import settings
from django.core.management import call_command
import requests
import urllib
import json
import sys
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def uploadScore_1(command, person):
	if isScoreManager(person):
		person.sendText('Please tell me the name of the hymn.')
		person.updateUserProgress('uploadScore_1')
		person.stageUp()

def uploadScore_2(command, person):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	if command != '/uploadscore': #principle: stage 2 blocks the bull
		if Scores.objects.filter(file_path=command+'.pdf').count() == 0:
			person.setStorage('uploadScore', {'hymn_name':command})
			person.sendText('Please upload the file here.')
			person.stageUp()
		else:
			person.sendText(command + ' has been uploaded already.')
			person.stageEnd()

def uploadScore_3(command, person):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	tmp = person.getStorage('uploadScore')
	tmp['file_id'] = command['file_id']
	person.setStorage('uploadScore', tmp)
	functions = []
	functions.append([InlineKeyboardButton(text='Upload', callback_data='/upload')])
	person.sendText('The score will be uploaded upon tapping Upload. Please tap cancel if the hymn name is wrong. \n\n Hymn Name: '+tmp['hymn_name'], functions)
	person.stageUp()

def uploadScore_4(command, person):
	if command == '/upload':
		tmp = person.getStorage('uploadScore')
		r = requests.get('https://api.telegram.org/bot'+settings.BOT_TOKEN+'/getFile?file_id='+ tmp['file_id'])
		result = json.loads(r.text)['result']
		file = urllib.URLopener()
		file.retrieve('https://api.telegram.org/file/bot'+settings.BOT_TOKEN+'/'+result['file_path'], settings.BASE_DIR+'/scores/'+tmp['hymn_name']+'.pdf')
		call_command('refreshScores')
		sendTextToScoreManagers('Score of ' + tmp['hymn_name'] + ' has been uploaded by '+ person.user_name)
		person.popStorage('uploadScore')
		person.stageEnd()
	else:
		functions = []
		functions.append([InlineKeyboardButton(text='Upload', callback_data='/upload')])
		person.sendText('The score will be uploaded upon tapping Upload. Please tap cancel if the hymn name is wrong. \n\n Hymn Name: '+tmp['hymn_name'], functions)
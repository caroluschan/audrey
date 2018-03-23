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

def uploadScore_1(command, person):
	if isScoreManager(person):
		person.updateUserProgress('uploadScore_1')
		person.stageUp()
		person.sendText('Please tell me the name of the hymn.')

def uploadScore_2(command, person):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	person.stageUp()
	person.setStorage('uploadScore', {'hymn_name':command})
	person.sendText('Please upload the file here.')

def uploadScore_3(command, person):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	person.stageUp()
	tmp = person.getStorage('uploadScore')
	tmp['file_id'] = command['file_id']
	person.setStorage('uploadScore', tmp)
	person.sendText('The score of '+ tmp['hymn_name'] +' will be uploaded upon tapping /upload')

def uploadScore_4(command, person):
	if command == '/upload':
		tmp = person.getStorage('uploadScore')
		r = requests.get('https://api.telegram.org/bot'+settings.BOT_TOKEN+'/getFile?file_id='+ tmp['file_id'])
		result = json.loads(r.text)['result']
		file = urllib.URLopener()
		file.retrieve('https://api.telegram.org/file/bot'+settings.BOT_TOKEN+'/'+result['file_path'], settings.BASE_DIR+'/scores/'+tmp['hymn_name']+'.pdf')
		call_command('refreshScores')
		person.sendText('Score of ' + tmp['hymn_name'] + ' has been uploaded')
		person.popStorage('uploadScore')
		person.stageEnd()
	else:
		person.sendText('The score of '+ tmp['hymn_name'] +' will be uploaded upon tapping /upload')
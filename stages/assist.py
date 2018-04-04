# -*- coding: utf-8 -*-
import string
import random
import sys
import os
import re
from django.conf import settings
from stages.models import *
from users.models import *
from stages.translations import *

#######################
####Assist Function####
#######################

def getAdmins():
	return Person.objects.filter(is_admin=True)

def getScoreManagers():
	return Person.objects.filter(is_score_manager=True)

def getScoreManagersNotAdmin():
	return Person.objects.filter(is_score_manager=True, is_admin=False)




def isAdmin(person):
	if person.is_admin:
		return True
	else:
		person.sendText("I'm sorry, only admin can make this request.")

def isScoreManager(person):
	if person.is_score_manager:
		return True
	else:
		person.sendText("I'm sorry, only score manager can make this request.")

def isApproved(person):
	if person.is_approved:
		return True
	else:
		person.sendText(person.user_name+", you will be notified when you signup is approved. If you cannot wait, please contact Admin.")





def findPersonByTelegramId(telegram_id):
	return Person.objects.filter(telegram_id=telegram_id)[0]

def id_generator(model, size=6, chars=string.ascii_uppercase + string.digits):
	identifier = None
	while True:
		identifier =  ''.join(random.choice(chars) for _ in range(size))
		if model.objects.filter(identifier=identifier).count() == 0:
			break
	return identifier




def sendTextToAdmins(message, keyboard=None):
	for admin in getAdmins():
			admin.sendText(message, keyboard)

def sendTextToScoreManagers(message, keyboard=None):
	for manager in getScoreManagers():
			manager.sendText(message, keyboard)

def sendTextToScoreManagersNotAdmin(message, keyboard=None):
	for manager in getScoreManagersNotAdmin():
			manager.sendText(message, keyboard)

def sendTextToAll(message, keyboard=None):
	for person in Person.objects.all():
			person.sendText(message, keyboard)




def isEnglish(s):
	try:
		s.encode(encoding='utf-8').decode('ascii')
	except UnicodeDecodeError:
		return False
	else:
		return True

def isDigit(s):
	numbers = ['1','2','3','4','5','6','7','8','9','0']
	return True if s in numbers else False

def strokeChecking(s):
	strokes = sorted(os.listdir(settings.BASE_DIR+'/stroke'))
	for stroke in strokes:
		with open(settings.BASE_DIR+'/stroke/'+stroke, 'r') as f:
			data = f.read()
			if s in data:
				return stroke
	return None


def translate(s, lang='cn', var={}):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	result = translations[s][lang]
	for k, v in var.iteritems():
		tmp = re.split(k, result)
		construct = ''
		for x in range(0,len(tmp)-1):
			construct += tmp[x]
			construct += v
		construct += tmp[len(tmp)-1]
		result = construct
	return result





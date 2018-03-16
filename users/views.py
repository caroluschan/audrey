# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from users.models import *
from stages.views import *
from stages.models import *
from django.conf import settings
import json
# Create your views here.

bot = telepot.Bot(settings.BOT_TOKEN)

######################
####Entry Function####
######################

@csrf_exempt
def handle(request):
	# chat_id = msg['chat']['id']
	# command = msg['text']
	data = json.loads(request.body)
	telegram_id = data['telegram_id']
	command = data['command'] #natural language mount point 1
	incomer = Person.objects.filter(telegram_id=telegram_id)
	if incomer.count() > 0:
		processCommand(command, incomer[0])
	elif command == "/start":
		bot.sendMessage(telegram_id, "Hello there! I am Audrey the Hymns Manager. Please signup first by tapping /signup in order for me to serve you!")
	elif command == "/signup":
		newUser = Person(telegram_id=telegram_id, is_admin=False, is_approved=False, stage_code=None, user_name=None)
		newUser.save()
		processCommand(command, newUser)
	else:
		bot.sendMessage(telegram_id, "Sorry, please signup by tapping /signup first before I can serve you.")
	return HttpResponse('200')

###############################
####Stage Control Functions####
###############################

def identifyStage(command):
	for door in settings.STAGES:
		if door['is_first']:
			if eval(door['command_pattern_check']):
				return door['stage_code']
	return None 

def executeStage(stage_code, command, person):
	if stage_code:
		for door in settings.STAGES:
			if door['stage_code'] == stage_code:
				exec(door['function_call'])
	else: 
		person.sendText("Sorry, I do not understand") #natural language mount point 2

def processCommand(command, person):
	executeStage(person.stage_code if person.stage_code and command != '/cancel' else identifyStage(command), command, person)
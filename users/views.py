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
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
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
		functions = []
		functions.append([InlineKeyboardButton(text=translate('SIGNUP','en'), callback_data='/signup_en')])
		functions.append([InlineKeyboardButton(text=translate('SIGNUP','cn'), callback_data='/signup_cn')])
		keyboard = InlineKeyboardMarkup(inline_keyboard=functions)
		bot.sendMessage(telegram_id, translate('START','cn'), reply_markup=keyboard)
	elif command[:7] == "/signup":
		newUser = Person(telegram_id=telegram_id, is_admin=False, is_approved=False,is_score_manager=False, stage_code=None, user_name=None, lang=command[-2:])
		newUser.save()
		processCommand(command, newUser)
	else:
		functions = []
		functions.append([InlineKeyboardButton(text=translate('SIGNUP','en'), callback_data='/signup_en')])
		functions.append([InlineKeyboardButton(text=translate('SIGNUP','cn'), callback_data='/signup_cn')])
		keyboard = InlineKeyboardMarkup(inline_keyboard=functions)
		bot.sendMessage(telegram_id, translate('PLEASE_SIGNUP', 'cn'), reply_markup=keyboard)

	if "query_id" in data:
		bot.answerCallbackQuery(data["query_id"], text=' ')
	return HttpResponse('200')

###############################
####Stage Control Functions####
###############################

def identifyStage(command):
	for door in settings.STAGES:
		if eval(door['command_pattern_check']):
			return door['stage_code']+'_1'
	return None 

def executeStage(stage_code, command, person):
	if stage_code:
		if command != '/cancel':
			exec(stage_code+'(command, person)')
		else:
			exec('cancel_1(command, person)')
	else: 
		person.sendText(translate('NOT_UNDERSTAND', person.lang)) #natural language mount point 2

def processCommand(command, person):
	executeStage(person.stage_code if person.stage_code and command != '/cancel' else identifyStage(command), command, person)
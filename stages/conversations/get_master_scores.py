# -*- coding: utf-8 -*-
from stages.models import *
from users.models import *
from stages.assist import *
from get_score_by_code import *
from django.conf import settings
from django.db import connection
import os
import sys
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

#Conversation: get master list of scores
def listScores_1(command, person): #command: /listscores | stage_code: listScores_1 | trigger: command == "/listscores"
	if isApproved(person):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		person.updateUserProgress('listScores_1')
		person.stageUp()
		connection.cursor()
		connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")
		message = translate('MASTER_SCORE_1', person.lang)
		strokes = sorted(os.listdir(settings.BASE_DIR+'/stroke'))
		line = 0
		buttons = []
		buttonline = []
		for stroke in strokes:
			buttonline.append(InlineKeyboardButton(text=translate('STROKE', person.lang, {'_num_': stroke}).encode('utf-8'), callback_data='/s' + stroke))
			line += 1
			if line == 4:
				buttons.append(buttonline)
				buttonline = []
				line = 0

		letters = Index.objects.filter(language='en').values('index')
		for letter in letters:
			# message += '/' + letter['index']
			buttonline.append(InlineKeyboardButton(text=letter['index'], callback_data='/' + letter['index']))
			line += 1
			if line == 4:
				buttons.append(buttonline)
				buttonline = []
				line = 0

		letters = Index.objects.filter(language='others').values('index')
		for letter in letters:
			# message += '/' + letter['index'] + '  '
			buttonline.append(InlineKeyboardButton(text=letter['index'], callback_data='/' + letter['index']))
			line += 1
			if line == 4:
				buttons.append(buttonline)
				buttonline = []
				line = 0
		if line != 0:
			buttons.append(buttonline)
			buttonline = []
			line = 0
		buttons.append([InlineKeyboardButton(text=translate('CANCEL_BTN', person.lang), callback_data='/cancel')])
		keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
		person.sendText(message, keyboard)


def listScores_2(command, person):
	try:
		if isApproved(person):
			person.stageUp()
			if command[:2] != '/s':
				listScores_3('/'+Index.objects.filter(index=command[1:])[0].identifier, person)
			else:
				reload(sys)
				sys.setdefaultencoding('utf-8')
				message = "========"+translate('STROKE', person.lang, {'_num_': command[2:]}).encode('utf-8')+"========"
				indexs = Index.objects.filter(language='cn').filter(stroke=command[2:])
				buttons = []
				buttonline = []
				line = 0
				for index in indexs:
					buttonline.append(InlineKeyboardButton(text=index.index, callback_data='/' + index.identifier))
					line += 1
					if line == 4:
						buttons.append(buttonline)
						buttonline = []
						line = 0
				if line != 0:
					buttons.append(buttonline)
					buttonline = []
					line = 0
				buttons.append([InlineKeyboardButton(text=translate('BACK', person.lang), callback_data='/back')])
				keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
				person.sendText(message, keyboard)
	except IndexError:
		person.sendText(translate('NOT_UNDERSTAND', person.lang))
		person.stageEnd()

def listScores_3(command, person):
	try:
		if isApproved(person):
			if command == '/back':
				listScores_1(command, person)
			elif command[:2] == '/s' or Index.objects.filter(index=command[1:]).count() > 0:
				person.stageDown()
				listScores_2(command,person)
			else:
				person.stageUp()
				reload(sys)
				sys.setdefaultencoding('utf-8')
				connection.cursor()
				connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")
				index = Index.objects.filter(identifier=command[1:])[0].index
				message = "===="+translate('LIST_OF_SCORE', person.lang,{'_index_': index}).encode('utf-8')+"===="
				scores = Scores.objects.filter(index=index).extra(select={'length':'Length(file_path)'}).order_by('length')
				buttons = []
				for score in scores:
					buttons.append([InlineKeyboardButton(text=score.file_path[:-4], callback_data='/songcode'+score.identifier)])
				keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
				person.sendText(message, keyboard)
				message = translate('ANOTHER_LETTER', person.lang)
				buttons = []
				buttons.append([InlineKeyboardButton(text=translate('YES', person.lang), callback_data='/Yes'), InlineKeyboardButton(text=translate('NO', person.lang), callback_data='/No')])
				keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
				person.sendText(message, keyboard)

	except IndexError:
		person.sendText(translate('NOT_UNDERSTAND', person.lang))
		person.stageEnd()

def listScores_4(command, person):
	if isApproved(person):
		if command[1:] == 'Yes':
			listScores_1(command, person)
		elif command[:9] == '/songcode':
			songCode_1(command,person)
			message = translate('ANOTHER_LETTER', person.lang)
			buttons = []
			buttons.append([InlineKeyboardButton(text=translate('YES', person.lang), callback_data='/Yes'), InlineKeyboardButton(text=translate('NO', person.lang), callback_data='/No')])
			keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
			person.sendText(message, keyboard)
		elif Index.objects.filter(identifier=command[1:]).count() > 0:
			person.stageDown()
			person.stageDown()
			listScores_3(command, person)
		elif command[1:] == 'No':
			person.sendText(translate('FOUND_SCORE', person.lang))
			person.stageEnd()
		elif command[:2] == '/s' or Index.objects.filter(index=command[1:]).count() > 0:
				person.stageDown()
				person.stageDown()
				listScores_2(command,person)
		else:
			person.sendText(translate('NOT_UNDERSTAND', person.lang))
			person.stageEnd()
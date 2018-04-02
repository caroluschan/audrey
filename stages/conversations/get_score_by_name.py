# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from stages.models import *
from users.models import *
from stages.assist import *
import sys
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

#Conversation: get score by lyrics    
def scoreByName_1(command, person): #command: /scorebyname | stage_code: scoreByName_1 | trigger: command == "/scorebyname"
	if isApproved(person):
		person.updateUserProgress('scoreByName_1')
		person.stageUp()
		person.sendText(translate('TELL_NAME', person.lang))

def scoreByName_2(command, person):
	if isApproved(person):
		person.sendText(translate('FETCH_SONG', person.lang))
		reload(sys)
		sys.setdefaultencoding('utf-8')
		matches = []
		words = command.replace('.',' ').replace(',',' ')
		if ' ' in words:
			words = words.split(' ')
		scoreCheck = Scores.objects
		for word in words:
			if word != '':
				scoreCheck = scoreCheck.filter(file_path__contains=word)
		if scoreCheck:
			for score in scoreCheck:
				matches.append(score)
		message = ''
		if len(matches) > 0:
			message += translate('I_THINK_THESE_ARE', person.lang)
			buttons = []
			history = []
			for score in matches:
				# if score.file_path[:-4] not in message:
					# message += score.file_path[:-4] + '\n' + translate('LINK', person.lang) + ': /songcode'+score.identifier + '\n\n'
				if score.file_path[:-4] not in history:	
					buttons.append([InlineKeyboardButton(text=score.file_path[:-4], callback_data='/songcode'+score.identifier)])
					history.append(score.file_path[:-4])
			keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
			person.sendText(message, keyboard)
		else:
			person.sendText( translate('NOT_FOUND_DOC_NAME', person.lang))
		person.stageEnd()
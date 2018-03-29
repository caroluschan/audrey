# -*- coding: utf-8 -*-
from stages.models import *
from users.models import *
from stages.assist import *
from get_score_by_code import *
from django.conf import settings
from django.db import connection
import os
import sys

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
		message += '------'+ translate('STROKES', person.lang).encode('utf-8')+'------\n\n'
		strokes = sorted(os.listdir(settings.BASE_DIR+'/stroke'))
		line = 0
		for stroke in strokes:
			message += '/s' + stroke + '  '
			line += 1
			if line == 6:
				message += '\n\n'
				line = 0
		if line != 0:
			message += '\n\n'

		message += '------' + translate('ALPHABET', person.lang).encode('utf-8') + '------\n\n'
		line = 0
		letters = Index.objects.filter(language='en').values('index')
		for letter in letters:
			message += '/' + letter['index'] + '  '
			line += 1
			if line == 10:
				message += '\n\n'
				line = 0
		if line != 0:
			message += '\n\n'

		message += '------' + translate('OTHERS', person.lang).encode('utf-8') + '------\n\n'
		line = 0
		letters = Index.objects.filter(language='others').values('index')
		for letter in letters:
			message += '/' + letter['index'] + '  '
			line += 1
			if line == 6:
				message += '\n\n'
				line = 0
		person.sendText(message)


def listScores_2(command, person):
	try:
		if isApproved(person):
			person.stageUp()
			if command[:2] != '/s':
				listScores_3('/'+Index.objects.filter(index=command[1:])[0].identifier, person)
			else:
				reload(sys)
				sys.setdefaultencoding('utf-8')
				message = '====' + command[2:] + translate('STROKE', person.lang).encode('utf-8') +'====\n\n'
				indexs = Index.objects.filter(language='cn').filter(stroke=command[2:])
				for index in indexs:
					message += index.index + '  /' + index.identifier +'\n'
				message += '\n' + translate('BACK', person.lang)
				person.sendText(message)
	except IndexError:
		person.sendText(translate('NOT_UNDERSTAND', person.lang))
		person.stageEnd()

def listScores_3(command, person):
	try:
		if isApproved(person):
			if command == translate('BACK', 'en'):
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
				message = '===='+translate('LIST_OF_SCORE', person.lang,{'_index_': index}).encode('utf-8') +'====\n\n'
				scores = Scores.objects.filter(index=index).extra(select={'length':'Length(file_path)'}).order_by('length')
				for score in scores:
					message += score.file_path[:-4] + '\n' + translate('LINK', person.lang)+': /songcode'+score.identifier + '\n\n'
				message += '\n\n' + translate('ANOTHER_LETTER', person.lang)
				person.sendText(message)
				
	except IndexError:
		person.sendText(translate('NOT_UNDERSTAND', person.lang))
		person.stageEnd()

def listScores_4(command, person):
	if isApproved(person):
		if command[1:] == 'Yes':
			listScores_1(command, person)
		elif command[:9] == '/songcode':
			songCode_1(command,person)
			person.sendText(translate('ANOTHER_LETTER', person.lang))
		elif Index.objects.filter(identifier=command[1:]).count() > 0:
			person.stageDown()
			person.stageDown()
			listScores_3(command, person)
		elif command[1:] == 'No:
			person.sendText(translate('FOUND_SCORE', person.lang))
			person.stageEnd()
		elif command[:2] == '/s' or Index.objects.filter(index=command[1:]).count() > 0:
				person.stageDown()
				person.stageDown()
				listScores_2(command,person)
		else:
			person.sendText(translate('NOT_UNDERSTAND', person.lang))
			person.stageEnd()
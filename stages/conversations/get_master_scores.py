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
		message = 'There are a lot of hymns my dear. What about choosing part of them first? The hymns will be ordered by the first letter of their name.\n\n'
		message += '------'+'筆劃'.encode('utf-8')+'------\n\n'
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

		message += '------Alphabet------\n\n'
		line = 0
		letters = Index.objects.filter(language='en').values('index')
		for letter in letters:
			message += '/' + letter['index'] + '  '
			line += 1
			if line == 7:
				message += '\n\n'
				line = 0
		if line != 0:
			message += '\n\n'

		message += '------Others------\n\n'
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
				message = '====' + command[2:] + '劃'.encode('utf-8') +'====\n\n'
				indexs = Index.objects.filter(language='cn').filter(stroke=command[2:])
				for index in indexs:
					message += index.index + '  /' + index.identifier +'\n'
				message += '\n/back'
				person.sendText(message)
	except IndexError:
		person.sendText("Sorry, I do not understand")
		person.stageEnd()

def listScores_3(command, person):
	try:
		if isApproved(person):
			if command[1:] != 'back':
				person.stageUp()
				reload(sys)
				sys.setdefaultencoding('utf-8')
				connection.cursor()
				connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")
				index = Index.objects.filter(identifier=command[1:])[0].index
				message = '====List of Scores for '+ index +'====\n\n'
				scores = Scores.objects.filter(index=index).extra(select={'length':'Length(file_path)'}).order_by('length')
				for score in scores:
					message += score.file_path[:-4] + '\n' + 'Link: /songcode'+score.identifier + '\n\n'
				message += '\n\n Search by another letter?\n/Yes        /No'
				person.sendText(message)
			else:
				listScores_1(command, person)
	except IndexError:
		person.sendText("Sorry, I do not understand")
		person.stageEnd()

def listScores_4(command, person):
	if isApproved(person):
		if command[1:] == 'Yes':
			listScores_1(command, person)
		elif command[:9] == '/songcode':
			person.stageEnd()
			songCode_1(command,person)
		elif Index.objects.filter(identifier=command[1:]).count() > 0:
			person.stageDown()
			person.stageDown()
			listScores_3(command, person)
		elif command[1:] == 'No':
			person.sendText('I hope you have found the hymn you need :)')
			person.stageEnd()
		else:
			person.sendText("Sorry, I do not understand")
			person.stageEnd()
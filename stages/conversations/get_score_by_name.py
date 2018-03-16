# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from stages.models import *
from users.models import *
from stages.assist import *
import sys

#Conversation: get score by lyrics    
def get_score_by_name_stage_1(command, person): #command: /scorebyname | stage_code: scoreByName_1 | trigger: command == "/scorebyname"
	if isApproved(person):
		person.updateUserProgress('scoreByName_1')
		person.stageUp()
		person.sendText("Please tell me the name of the song.")

def get_score_by_name_stage_2(command, person):
	if isApproved(person):
		person.sendText("OK let me go find it in the library. May take a while")
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
			message += 'I think these hymns are the ones you are looking for: \n\n'
			for score in matches:
				if score.file_path[:-4] not in message:
					message += score.file_path[:-4] + '\n' + 'Link: /songcode'+score.identifier + '\n\n'
			person.sendText(message)
		else:
			person.sendText('I am sorry :( I cannot find a hymn with this name')
		person.stageEnd()
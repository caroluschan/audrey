from stages.models import *
from users.models import *
from stages.assist import *
from get_score_by_code import *
from django.conf import settings
from django.db import connection
import os
import sys

#Conversation: get master list of scores
def get_master_scores_stage_1(command, person): #command: /listscores | stage_code: listScores_1 | trigger: command == "/listscores"
	if isApproved(person):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		person.updateUserProgress('listScores_1')
		person.stageUp()
		connection.cursor()
		connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")
		message = 'There are a lot of hymns my dear. What about choosing part of them first? The hymns will be ordered by the first letter of their name.\n\n'
		indexs = Scores.objects.values('index').distinct()
		for index in indexs:
			message += index['index'] + '  /' + Index.objects.filter(index=index['index'])[0].identifier +'\n'
		person.sendText(message)


def get_master_scores_stage_2(command, person):
	if isApproved(person):
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

def get_master_scores_stage_3(command, person):
	if isApproved(person):
		if command[1:] == 'Yes':
			get_master_scores_stage_1(command, person)
		elif command[:9] == '/songcode':
			person.stageEnd()
			get_score_by_code_stage_1(command,person)
		elif Index.objects.filter(identifier=command[1:]).count() > 0:
			person.stageDown()
			get_master_scores_stage_2(command, persons)
		else:
			person.sendText('I hope you have found the hymn you need :)')
			person.stageEnd()
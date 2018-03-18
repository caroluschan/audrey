# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from stages.models import *
from users.models import *
from stages.assist import *
from django.conf import settings
from google import google
import operator
import sys

#Conversation: get score by lyrics    
def get_score_by_lyrics_stage_1(command, person): #command: /scorebylyrics | stage_code: scorebylyrics_1 | trigger: command[:14] == "/scorebylyrics"
	if isApproved(person):
		person.updateUserProgress('scoreByLyrics_1')
		person.stageUp()
		person.sendText("Please tell me the lyrics.")


def get_score_by_lyrics_stage_2(command, person):
	if isApproved(person):
		person.sendText("OK let me go find it in the library. May take a while")
		reload(sys)
		sys.setdefaultencoding('utf-8')
		keyword = command + ' site:christianstudy.com/data/hymns/text'
		searchResult = google.search(keyword, 1, 'zh-CN')
		results = []
		matches = []
		if searchResult:
			for x in range(0,len(searchResult)):
				results.append(searchResult[x].name[1:-1] if searchResult[x].name[:1] == '【' else searchResult[x].name)
			print(results)
			for result in results:
				directCheck = Scores.objects.filter(file_path__contains=result)
				if directCheck.count() > 0:
					matches.append(directCheck[0])
				else:
					words = result.replace('.',' ').replace(',',' ')
					if ' ' in result:
						words = result.split(' ')
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
			person.sendText('I am sorry :( I cannot find a hymn with this lyrics')
		person.stageEnd()

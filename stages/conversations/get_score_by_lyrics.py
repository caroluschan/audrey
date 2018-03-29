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
def scoreByLyrics_1(command, person): #command: /scorebylyrics | stage_code: scorebylyrics_1 | trigger: command[:14] == "/scorebylyrics"
	if isApproved(person):
		person.updateUserProgress('scoreByLyrics_1')
		person.stageUp()
		person.sendText(translate('LYRICS', person.lang))


def scoreByLyrics_2(command, person):
	if isApproved(person):
		person.sendText(translate('FETCH_SONG', person.lang))
		reload(sys)
		sys.setdefaultencoding('utf-8')
		keyword = command + ' site:christianstudy.com/data/hymns/text'
		searchResult = google.search(keyword, 1, 'zh-CN')
		results = []
		matches = []
		if searchResult:
			for x in range(0,len(searchResult)):
				results.append(searchResult[x].name[searchResult[x].name.find('【')+1:searchResult[x].name.find('】')] if searchResult[x].name.find('【') != -1 else searchResult[x].name)
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
			message += translate('I_THINK_THESE_ARE', person.lang)
			for score in matches:
				if score.file_path[:-4] not in message:
					message += score.file_path[:-4] + '\n' + translate('LINK', person.lang) + ': /songcode'+score.identifier + '\n\n'
			person.sendText(message)
		else:
			person.sendText(translate('NOT_FOUND_DOC_NAME', person.lang))
		person.stageEnd()

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from stages.models import *
from users.models import *
from stages.assist import *
from django.conf import settings
import googlesearch as google
import operator
import sys
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

#Conversation: get score by lyrics    
def scoreByLyrics_1(command, person): #command: /scorebylyrics | stage_code: scorebylyrics_1 | trigger: command[:14] == "/scorebylyrics"
	if isApproved(person):
		person.sendText(translate('TELL_LYRICS', person.lang))
		person.updateUserProgress('scoreByLyrics_1')
		person.stageUp()


def scoreByLyrics_2(command, person):
	if isApproved(person):
		person.sendText(translate('FETCH_SONG', person.lang),with_cancel=False)
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
				# if directCheck.count() > 0:
				# 	matches.append(directCheck[0])
				# else:
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
			buttons = []
			history = []
			for score in matches:
				if score.file_path[:-4] not in history:	
					buttons.append([InlineKeyboardButton(text=score.file_path[:-4], callback_data='/songcode'+score.identifier)])
					history.append(score.file_path[:-4])
			person.sendText(message, buttons,with_cancel=False)
		else:
			person.sendText(translate('NOT_FOUND_DOC_NAME', person.lang),with_cancel=False)
		person.stageEnd()

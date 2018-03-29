# -*- coding: utf-8 -*-
from stages.models import *
from users.models import *
from stages.assist import *
import sys

def changeLang_1(command, person):
	if isApproved(person):
		person.updateUserProgress('changeLang_1')
		person.stageUp()
		person.sendText(translate('LANG_MENU', person.lang))

def changeLang_2(command, person):
	if isApproved(person):
		if command == "/English":
			person.setLang('en')
			person.sendText(translate('SET_LANG', person.lang, {'_lang_': translate('ENGLISH', person.lang)}))
			person.stageEnd()
		elif command == "/Chinese":
			person.setLang('cn')
			person.sendText(translate('SET_LANG', person.lang, {'_lang_': translate('CHINESE', person.lang)}))
			person.stageEnd()
		else:
			changeLang_1(command, person)
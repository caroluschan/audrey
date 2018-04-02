# -*- coding: utf-8 -*-
from stages.models import *
from users.models import *
from stages.assist import *
import sys
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def changeLang_1(command, person):
	if isApproved(person):
		person.updateUserProgress('changeLang_1')
		person.stageUp()
		functions = []
		functions.append([InlineKeyboardButton(text=translate('ENGLISH',person.lang), callback_data='/English')])
		functions.append([InlineKeyboardButton(text=translate('CHINESE',person.lang), callback_data='/Chinese')])
		keyboard = InlineKeyboardMarkup(inline_keyboard=functions)
		person.sendText(translate('LANG_MENU', person.lang), keyboard)

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
from users.models import *
from stages.views import *
from stages.models import *
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def listScoreManagerFunctions_1(command,person):
	if isScoreManager(person):
		functions = []
		functions.append([InlineKeyboardButton(text='List Score Manager', callback_data='/listscoremanagers')])
		functions.append([InlineKeyboardButton(text='Upload Score', callback_data='/uploadscore')])

		message = '===Score Manager Menu==='


		person.sendText(message, functions,with_cancel=False)
from users.models import *
from stages.views import *
from stages.models import *
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def listAdminFunctions_1(command,person):
	if isAdmin(person):
		functions = []
		functions.append([InlineKeyboardButton(text='List Users', callback_data='/listusers')])
		functions.append([InlineKeyboardButton(text='Rename User', callback_data='/renameuser')])
		functions.append([InlineKeyboardButton(text='Delete User', callback_data='/deleteuser')])
		functions.append([InlineKeyboardButton(text='List Admins', callback_data='/listadmins')])
		functions.append([InlineKeyboardButton(text='Set Admin', callback_data='/setadmin')])
		functions.append([InlineKeyboardButton(text='Unset Admin', callback_data='/unsetadmin')])
		functions.append([InlineKeyboardButton(text='List Score Manager', callback_data='/listscoremanagers')])
		functions.append([InlineKeyboardButton(text='Set Score Manager', callback_data='/setscoremanager')])
		functions.append([InlineKeyboardButton(text='Unset Score Manager', callback_data='/unsetscoremanager')])
		functions.append([InlineKeyboardButton(text='Announcement', callback_data='/announcement')])

		keyboard = InlineKeyboardMarkup(inline_keyboard=functions)

		message = '====Admin Menu===='

		person.sendText(message, keyboard)
from stages.models import *
from users.models import *
from stages.assist import *

def announcement_1(command, person):
	if isAdmin(person):
		functions = []
		functions.append([InlineKeyboardButton(text='Public', callback_data='/Public')])
		functions.append([InlineKeyboardButton(text='Admin', callback_data='/Admin')])
		functions.append([InlineKeyboardButton(text='Score Manager', callback_data='/ScoreManager')])
		person.sendText('Who are the audiences?', functions)
		person.updateUserProgress('announcement_1')
		person.stageUp()

def announcement_2(command, person):
	if command[1:] == 'Public' or command[1:] == 'Admin' or command[1:] == 'ScoreManager':
		person.setStorage('announcement',{'audiences':command[1:]})
		functions = []
		functions.append([InlineKeyboardButton(text='Yes', callback_data='/Yes')])
		functions.append([InlineKeyboardButton(text='No', callback_data='/No')])
		person.sendText('Do you want your name be shown?', functions)
		person.stageUp()
	else:
		person.sendText('I do not understand.',with_cancel=False)
		person.stageDown()
		announcement_1(command, person)

def announcement_3(command, person):
	if command[1:] == 'Yes' or command[1:] == 'No':
		person.stageUp()
		tmp = person.getStorage('announcement')
		tmp['named'] = True if command[1:] == 'Yes' else False
		person.setStorage('announcement', tmp)
		person.sendText('Tell me the announcement to be made.')
	else:
		functions = []
		functions.append([InlineKeyboardButton(text='Yes', callback_data='/Yes')])
		functions.append([InlineKeyboardButton(text='No', callback_data='/No')])
		person.sendText('Do you want your name be shown?', functions)
		person.stageDown()

def announcement_4(command, person):
	person.stageUp()
	tmp = person.getStorage('announcement')
	tmp['message'] = command
	person.setStorage('announcement', tmp)
	functions = []
	functions.append([InlineKeyboardButton(text='Send', callback_data='/send')])
	person.sendText('Announcement will be made as soon as you tap Send.', functions)


def announcement_5(command, person):
	if command[1:] == 'send':
		tmp = person.getStorage('announcement')
		message = ''

		if tmp['audiences'] == 'Public':
			message += '==Public Announcement==\n\n'
		elif tmp['audiences'] == 'Admin':
			message += '==Admin Internal Announcement==\n\n'
		elif tmp['audiences'] == 'ScoreManager':
			message += '==Score Manager Internal Announcement==\n\n'

		message += tmp['message']

		if tmp['named']:
			message += '\n\n' + person.user_name
		if tmp['audiences'] == 'Public':
			sendTextToAll(message)
		elif tmp['audiences'] == 'Admin':
			sendTextToAdmins(message)
		elif tmp['audiences'] == 'ScoreManager':
			sendTextToScoreManagers(message)
			
		person.sendText('Your announcement has been made', with_cancel=False)
		person.stageEnd()
		person.popStorage('announcement')
	else:
		functions = []
		functions.append([InlineKeyboardButton(text='Send', callback_data='/send')])
		person.sendText('Announcement will be made as soon as you tap Send.', functions)


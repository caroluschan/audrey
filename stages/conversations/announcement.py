from stages.models import *
from users.models import *
from stages.assist import *

def announcement_1(command, person):
	if isAdmin(person):
		person.updateUserProgress('announcement_1')
		person.stageUp()
		person.sendText('Who are the audiences?\n\n/Public        /Admin\n\n/cancel')

def announcement_2(command, person):
	if command[1:] == 'Public' or command[1:] == 'Admin':
		person.setStorage('announcement',{'audiences':command[1:]})
		person.stageUp()
		person.sendText('Do you want your name be shown?\n\n/Yes        /No\n\n/cancel')
	elif command[1:] == 'cancel':
		person.stageEnd()
		person.sendText('Your request has been cancelled.')
	else:
		person.sendText('I do not understand.')
		person.stageDown()
		announcement_1(command, person)

def announcement_3(command, person):
	if command[1:] == 'Yes' or command[1:] == 'No':
		person.stageUp()
		tmp = person.getStorage('announcement')
		tmp['named'] = True if command[1:] == 'Yes' else False
		person.setStorage('announcement', tmp)
		person.sendText('Tell me the announcement to be made.\n\n/cancel')
	elif command[1:] == 'cancel':
		person.stageEnd()
		person.popStorage('announcement')
		person.sendText('Your request has been cancelled.')
	else:
		person.stageDown()
		person.sendText('Do you want your name be shown?\n\n/Yes        /No\n\n/cancel')

def announcement_4(command, person):
	if command[1:] != 'cancel':
		person.stageUp()
		tmp = person.getStorage('announcement')
		tmp['message'] = command
		person.setStorage('announcement', tmp)
		person.sendText('Announcement will be made as soon as you tap /send.\n\n/cancel')
	else:
		person.stageEnd()
		person.popStorage('announcement')
		person.sendText('Your request has been cancelled.')

def announcement_5(command, person):
	if command[1:] == 'send':
		tmp = person.getStorage('announcement')
		message = ''
		if tmp['audiences'] == 'Public':
			message += '==Public Announcement==\n\n'
		elif tmp['audiences'] == 'Admin':
			message += '==Admin Internal Announcement==\n\n'
		message += tmp['message']
		if tmp['named']:
			message += '\n\n' + person.user_name
		if tmp['audiences'] == 'Public':
			sendTextToAll(message)
		elif tmp['audiences'] == 'Admin':
			sendTextToAdmins(message)
		person.sendText('Your announcement has been made')
		person.stageEnd()
		person.popStorage('announcement')
	elif command[1:] == 'cancel':
		person.stageEnd()
		person.popStorage('announcement')
		person.sendText('Your request has been cancelled.')
	else:
		person.sendText('Announcement will be made as soon as you tap /send.\n\n/cancel')


from stages.models import *
from users.models import *
from stages.assist import *

def deleteUser_1(command, person): #command: /deleteuser | stage_code: deleteUser_1 | trigger: command == "/deleteuser"
	if isAdmin(person):
		lou = Person.objects.all()
		message = 'Please choose the user to be deleted'
		functions = []
		for user in lou:
			functions.append([InlineKeyboardButton(text=user.user_name, callback_data='/'+user.telegram_id)])
		person.sendText(message, functions)
		person.updateUserProgress('deleteUser_1')
		person.stageUp()

def deleteUser_2(command, person):
	target = Person.objects.filter(telegram_id=command[1:])

	if target:
		if target[0].is_admin == False:
			victum = target[0].user_name
			target[0].delete()
			sendTextToAdmins(victum+"'s account has been deleted by "+person.user_name,with_cancel=False)
		else:
			person.sendText('Sorry, please unset the user\'s Admin right before deleting',with_cancel=False)
	else:
		person.sendText('Sorry, user not found',with_cancel=False)
	person.stageEnd()
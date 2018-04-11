from stages.models import *
from users.models import *
from stages.assist import *

def listUsers_1(command, person): #command: /listusers | stage_code: listusers_1 | trigger: command == "/listusers"
	if isAdmin(person):
		lou = Person.objects.all()
		message = '==List of Users==\n\nName\tTelegram ID\n'
		for user in lou:
			message += user.user_name + '\t' + user.telegram_id + '\n'
		person.sendText(message,with_cancel=False)
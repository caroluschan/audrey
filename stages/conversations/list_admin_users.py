from stages.models import *
from users.models import *
from stages.assist import *

#Conversation: list admin users
def list_admin_users_stage_1(command, person): #command: /listadmins | stage_code: listadmins_1 | trigger: command == "/listadmins"
	if isAdmin(person):
		lou = Person.objects.filter(is_admin=True)
		message = '==List of Admins==\n\nName\tTelegram ID\n'
		for user in lou:
			message += user.user_name + '\t' + user.telegram_id + '\n'
		person.sendText(message)
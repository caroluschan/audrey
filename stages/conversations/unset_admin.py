from stages.models import *
from users.models import *
from stages.assist import *
from django.conf import settings

def unsetAdmin_1(command, person):
	if isAdmin(person):
		person.updateUserProgress('unsetAdmin_1')
		person.stageUp()
		lou = Person.objects.filter(is_admin=True).exclude(telegram_id=settings.SUPERADMIN)
		message = ''
		if lou:
			message += 'Which admin to unset?\n\n'
			for user in lou:
				message += user.user_name + '\t/' + user.telegram_id + '\n'
		else:
			message += 'There is no admin to be unset.'
			person.stageEnd()
		person.sendText(message)

def unsetAdmin_2(command, person):
	target = Person.objects.filter(telegram_id=command[1:])[0]
	target.unsetAsAdmin()
	target.sendText(target.user_name + ' has been unset as admin by ' + person.user_name)
	sendTextToAdmins(target.user_name + ' has been unset as admin by ' + person.user_name)
	person.stageEnd()



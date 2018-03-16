from stages.models import *
from users.models import *
from stages.assist import *
from django.conf import settings

def set_admin_stage_1(command, person):
	if isAdmin(person):
		person.updateUserProgress('setAdmin_1')
		person.stageUp()
		lou = Person.objects.filter(is_admin=False).exclude(telegram_id=settings.SUPERADMIN)
		message = ''
		if lou:
			message += 'Which user to do you want to set as admin?\n\n'
			for user in lou:
				message += user.user_name + '\t/' + user.telegram_id + '\n'
		else:
			message += 'There is no other users to be set as admin.'
			person.stageEnd()
		person.sendText(message)

def set_admin_stage_2(command, person):
	target = Person.objects.filter(telegram_id=command[1:])[0]
	target.setAsAdmin()
	sendTextToAdmins(target.user_name + ' has been set as admin by ' + person.user_name)
	person.stageEnd()

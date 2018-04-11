from stages.models import *
from users.models import *
from stages.assist import *
from django.conf import settings

def setAdmin_1(command, person):
	if isAdmin(person):
		lou = Person.objects.filter(is_admin=False).exclude(telegram_id=settings.SUPERADMIN)
		functions = []
		if lou:
			message = 'Which user to do you want to set as admin?'
			for user in lou:
				functions.append([InlineKeyboardButton(text=user.user_name, callback_data=user.telegram_id)])
			person.sendText(message, functions)
		else:
			message = 'There is no other users to be set as admin.'
			person.sendText(message,with_cancel=False)
			person.stageEnd()
		person.updateUserProgress('setAdmin_1')
		person.stageUp()

def setAdmin_2(command, person):
	target = Person.objects.filter(telegram_id=command[1:])[0]
	target.setAsAdmin()
	sendTextToAdmins(target.user_name + ' has been set as admin by ' + person.user_name,with_cancel=False)
	person.stageEnd()

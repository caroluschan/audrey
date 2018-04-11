from stages.models import *
from users.models import *
from stages.assist import *
from django.conf import settings

def unsetAdmin_1(command, person):
	if isAdmin(person):
		lou = Person.objects.filter(is_admin=True).exclude(telegram_id=settings.SUPERADMIN)
		if lou:
			message = 'Which admin to unset?'
			for user in lou:
				functions.append([InlineKeyboardButton(text=user.user_name, callback_data=user.telegram_id)])
			person.sendText(message, functions)
		else:
			message = 'There is no admin to be unset.'
			person.sendText(message,with_cancel=False)
			person.stageEnd()
		person.updateUserProgress('unsetAdmin_1')
		person.stageUp()

def unsetAdmin_2(command, person):
	target = Person.objects.filter(telegram_id=command[1:])[0]
	target.unsetAsAdmin()
	target.sendText(target.user_name + ' has been unset as admin by ' + person.user_name,with_cancel=False)
	sendTextToAdmins(target.user_name + ' has been unset as admin by ' + person.user_name,with_cancel=False)
	person.stageEnd()



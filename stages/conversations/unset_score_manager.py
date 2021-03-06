from stages.models import *
from users.models import *
from stages.assist import *
from django.conf import settings

def unsetScoreManager_1(command, person):
	if isAdmin(person):
		lou = Person.objects.filter(is_score_manager=True).exclude(telegram_id=settings.SUPERADMIN)
		functions = []
		if lou:
			message = 'Which score manager to unset?'
			for user in lou:
				functions.append([InlineKeyboardButton(text=user.user_name, callback_data='/'+user.telegram_id)])
			person.sendText(message, functions)
		else:
			message = 'There is no score manager to be unset.'
			person.sendText(message,with_cancel=False)
			person.stageEnd()
		person.updateUserProgress('unsetScoreManager_1')
		person.stageUp()

def unsetScoreManager_2(command, person):
	target = Person.objects.filter(telegram_id=command[1:])[0]
	target.unsetAsScoreManager()
	target.sendText(target.user_name + ' has been unset as score manager by ' + person.user_name,with_cancel=False)
	sendTextToAdmins(target.user_name + ' has been unset as score manager by ' + person.user_name,with_cancel=False)
	sendTextToScoreManagersNotAdmin(target.user_name + ' has been unset as score manager by ' + person.user_name,with_cancel=False)
	person.stageEnd()

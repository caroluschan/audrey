from stages.models import *
from users.models import *
from stages.assist import *
from django.conf import settings

def setScoreManager_1(command, person):
	if isAdmin(person):
		lou = Person.objects.filter(is_score_manager=False).exclude(telegram_id=settings.SUPERADMIN)
		functions = []
		if lou:
			message = 'Which user to do you want to set as score manager?'
			for user in lou:
				functions.append([InlineKeyboardButton(text=user.user_name, callback_data='/'+user.telegram_id)])
			person.sendText(message, functions)
		else:
			message = 'There is no other users to be set as score manager.'
			person.sendText(message,with_cancel=False)
			person.stageEnd()
		person.updateUserProgress('setScoreManager_1')
		person.stageUp()

def setScoreManager_2(command, person):
	target = Person.objects.filter(telegram_id=command.replace('/', ''))[0]
	target.setAsScoreManager()
	sendTextToAdmins(target.user_name + ' has been set as score manager by ' + person.user_name,with_cancel=False)
	sendTextToScoreManagersNotAdmin(target.user_name + ' has been set as score manager by ' + person.user_name,with_cancel=False)
	person.stageEnd()

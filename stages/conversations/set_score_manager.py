from stages.models import *
from users.models import *
from stages.assist import *
from django.conf import settings

def setScoreManager_1(command, person):
	if isAdmin(person):
		person.updateUserProgress('setScoreManager_1')
		person.stageUp()
		lou = Person.objects.filter(is_score_manager=False).exclude(telegram_id=settings.SUPERADMIN)
		message = ''
		if lou:
			message += 'Which user to do you want to set as score manager?\n\n'
			for user in lou:
				message += user.user_name + '\t/' + user.telegram_id + '\n'
		else:
			message += 'There is no other users to be set as score manager.'
			person.stageEnd()
		person.sendText(message)

def setScoreManager_2(command, person):
	target = Person.objects.filter(telegram_id=command[1:])[0]
	target.setAsScoreManager()
	sendTextToAdmins(target.user_name + ' has been set as score manager by ' + person.user_name)
	sendTextToScoreManagersNotAdmin(target.user_name + ' has been set as score manager by ' + person.user_name)
	person.stageEnd()

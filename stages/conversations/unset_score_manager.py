from stages.models import *
from users.models import *
from stages.assist import *
from django.conf import settings

def unset_score_manager_stage_1(command, person):
	if isAdmin(person):
		person.updateUserProgress('unsetScoreManager_1')
		person.stageUp()
		lou = Person.objects.filter(is_score_manager=True).exclude(telegram_id=settings.SUPERADMIN)
		message = ''
		if lou:
			message += 'Which score manager to unset?\n\n'
			for user in lou:
				message += user.user_name + '\t/' + user.telegram_id + '\n'
		else:
			message += 'There is no score manager to be unset.'
			person.stageEnd()
		person.sendText(message)

def unset_score_manager_stage_2(command, person):
	target = Person.objects.filter(telegram_id=command[1:])[0]
	target.unsetAsScoreManager()
	target.sendText(target.user_name + ' has been unset as score manager by ' + person.user_name)
	sendTextToAdmins(target.user_name + ' has been unset as score manager by ' + person.user_name)
	sendTextToScoreManagersNotAdmin(target.user_name + ' has been unset as score manager by ' + person.user_name)
	person.stageEnd()

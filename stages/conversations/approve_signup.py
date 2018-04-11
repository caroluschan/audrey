from stages.models import *
from users.models import *
from stages.assist import *

#Conversation: user approval
def approve_1(command, person): #command: /approve[telegram_id] | stage_code: approve_1 | trigger: command[:8] == "/approve"
	if isAdmin(person):
		user = findPersonByTelegramId(command[8:])
		if user.is_approved is False:
			user.approve()
			user.stageEnd()
			user.sendText(translate('SIGNUP_APPROVED', person.lang), with_cancel=False)
			for admin in getAdmins():
				admin.sendText(person.user_name+" has approved the application of "+user.user_name+".", with_cancel=False)
		else:
			person.sendText('User has been approved', with_cancel=False)
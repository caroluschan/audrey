from stages.models import *
from users.models import *
from stages.assist import *

#Conversation: user approval
def approve_1(command, person): #command: /approve[telegram_id] | stage_code: approve_1 | trigger: command[:8] == "/approve"
	if isAdmin(person):
		user = findPersonByTelegramId(command[8:])
		user.approve()
		user.stageEnd()
		user.sendText("Your signup is approved! I am now at your service my dear. Please tap the [ / ] button by the left of the send button for my utilities. ")
		for admin in getAdmins():
			admin.sendText(person.user_name+" has approved the application of "+user.user_name+".")
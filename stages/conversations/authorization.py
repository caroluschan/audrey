from stages.models import *
from users.models import *
from stages.assist import *

#Conversation: authorization
def auth_1(command, person):
	if person.user_name == None:
		person.updateUserProgress('auth_1')
		person.stageUp()
		person.sendText("Hello! What is your name?")
	else:
		person.sendText(translate("SIGNUP_ALREADY", person.lang))
		
def auth_2(command, person): #command: [name] | stage_code: auth_2
	if Person.objects.filter(user_name=command).count() > 0:
		person.sendText('I\'m sorry :( This name has been used. Please make up another one.')
	else:
		person.setName(command)
		person.stageUp()
		person.sendText("Nice to meet you, "+command+". Your signup is well received. You will be notified when you signup is approved.")
		sendTextToAdmins(command+" has signed up.\n/approve"+person.telegram_id)

def auth_3(command, person): #command: ??? | stage_code: auth_3
	person.sendText(person.user_name+", you will be notified when you signup is approved. If you cannot wait, please contact Charles.")
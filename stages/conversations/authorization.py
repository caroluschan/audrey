from stages.models import *
from users.models import *
from stages.assist import *

#Conversation: authorization
def auth_1(command, person):
	if person.user_name == None:
		person.updateUserProgress('auth_1')
		person.stageUp()
		person.sendText(translate("YOUR_NAME", person.lang))
	else:
		person.sendText(translate("SIGNUP_ALREADY", person.lang))
		
def auth_2(command, person): #command: [name] | stage_code: auth_2
	if Person.objects.filter(user_name=command).count() > 0:
		person.sendText(translate('DUPLICATED_NAME', person.lang))
	else:
		person.setName(command)
		person.stageUp()
		person.sendText(translate('NAME_RECEIVED', person.lang, {'_name_': command}))
		functions = []
		functions.append([InlineKeyboardButton(text='Approve', callback_data="/approve"+person.telegram_id)])
		keyboard = InlineKeyboardMarkup(inline_keyboard=functions)
		sendTextToAdmins(command+" has signed up.", keyboard)

def auth_3(command, person): #command: ??? | stage_code: auth_3
	person.sendText(translate('NOT_APPROVED_YET', person.lang, {'_name_': person.user_name}))
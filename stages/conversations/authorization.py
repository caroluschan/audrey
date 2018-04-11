from stages.models import *
from users.models import *
from stages.assist import *
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

#Conversation: authorization
def auth_1(command, person):
	if person.user_name == None:
		person.sendText(translate("YOUR_NAME", person.lang), with_cancel=False)
		person.updateUserProgress('auth_1')
		person.stageUp()
	else:
		person.sendText(translate("SIGNUP_ALREADY", person.lang), with_cancel=False)
		
def auth_2(command, person): #command: [name] | stage_code: auth_2
	if Person.objects.filter(user_name=command).count() > 0:
		person.sendText(translate('DUPLICATED_NAME', person.lang), with_cancel=False)
	else:
		person.setName(command)
		person.sendText(translate('NAME_RECEIVED', person.lang, {'_name_': command}), with_cancel=False)
		person.stageUp()
		functions = []
		functions.append([InlineKeyboardButton(text='Approve', callback_data="/approve"+person.telegram_id)])
		sendTextToAdmins(command+" has signed up.", functions, with_cancel=False)

def auth_3(command, person): #command: ??? | stage_code: auth_3
	person.sendText(translate('NOT_APPROVED_YET', person.lang, {'_name_': person.user_name}), with_cancel=False)
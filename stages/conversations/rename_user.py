from stages.models import *
from users.models import *
from stages.assist import *

def renameUser_1(command, person):
	if isAdmin(person):
		message = 'Who\'s name would you like to change?'
		lou = Person.objects.all()
		functions = []
		for user in lou:
			functions.append([InlineKeyboardButton(text=user.user_name, callback_data='/'+user.telegram_id)])
		person.sendText(message, functions)
		person.updateUserProgress('renameUser_1')
		person.stageUp()

def renameUser_2(command, person):
	if Person.objects.filter(telegram_id=command[1:]).count() > 0:
		person.setStorage('renameUser',{'telegram_id':command[1:]})
		person.sendText('What will be the new name?',with_cancel=False)
		person.stageUp()
	else:
		person.sendText('User does not exist.',with_cancel=False)
		person.stageEnd()

def renameUser_3(command, person):
	target = Person.objects.filter(telegram_id=person.getStorage('renameUser')['telegram_id'])[0]
	oldName = target.user_name
	target.setName(command)
	person.popStorage('renameUser')
	person.sendText(oldName + '\'s account name has been changed to ' + command,with_cancel=False)
	person.stageEnd()
	target.sendText(translate('NAME_CHANGED_TARGET', target.lang, {"_old_":oldName, "_new_":command}),with_cancel=False)

from stages.models import *
from users.models import *
from stages.assist import *

def rename_user_stage_1(command, person):
	if isAdmin(person):
		person.updateUserProgress('renameUser_1')
		person.stageUp()
		message = 'Who\'s name would you like to change?\n\n'
		lou = Person.objects.all()
		for user in lou:
			message += user.user_name + '\t/' + user.telegram_id + '\n'
		person.sendText(message)

def rename_user_stage_2(command, person):
	if Person.objects.filter(telegram_id=command[1:]).count() > 0:
		person.stageUp()
		person.setStorage('renameUser',{'telegram_id':command[1:]})
		person.sendText('What will be the new name?')
	else:
		person.sendText('User does not exist.')
		person.stageEnd()

def rename_user_stage_3(command, person):
	target = Person.objects.filter(telegram_id=person.getStorage('renameUser')['telegram_id'])[0]
	oldName = target.user_name
	target.setName(command)
	person.popStorage('renameUser')
	person.sendText(oldName + '\'s account name has been changed to ' + command)
	person.stageEnd()

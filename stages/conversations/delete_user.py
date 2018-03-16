from stages.models import *
from users.models import *
from stages.assist import *

def delete_user_stage_1(command, person): #command: /deleteuser | stage_code: deleteUser_1 | trigger: command == "/deleteuser"
	if isAdmin(person):
		person.updateUserProgress('deleteUser_1')
		person.stageUp()
		lou = Person.objects.all()
		message = 'Please choose the user to be deleted\n\n'
		for user in lou:
			message += user.user_name + '\t/' + user.telegram_id +  '\n'
		person.sendText(message)

def delete_user_stage_2(command, person):
	target = Person.objects.filter(telegram_id=command[1:])

	if target:
		if target[0].is_admin == False:
			victum = target[0].user_name
			target[0].delete()
			sendTextToAdmins(victum+"'s account has been deleted by "+person.user_name)
		else:
			person.sendText('Sorry, please unset the user\'s Admin right before deleting')
	else:
		person.sendText('Sorry, user not found')
	person.stageEnd()
from users.models import *
from stages.views import *
from stages.models import *

def list_admin_functions_stage_1(command,person):
	if isScoreManager(person):
		functions = []
		functions.append('List Users: /listusers\n')
		functions.append('Rename User: /renameuser\n')
		functions.append('Delete User: /deleteuser\n')
		functions.append('List Admins: /listadmins\n')
		functions.append('Set Admin: /setadmin\n')
		functions.append('Unset Admin:/unsetadmin\n')
		functions.append('List Score Manager:/listscoremanagers\n')
		functions.append('Set Score Manager: /setscoremanager\n')
		functions.append('Unset Score Manager:/unsetscoremanager\n')
		functions.append('Announcement: /announcement\n')

		message = '====Admin Menu====\n\n'

		for function in functions:
			message += function

		person.sendText(message)
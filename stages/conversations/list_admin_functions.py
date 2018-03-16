from users.models import *
from stages.views import *
from stages.models import *

def list_admin_functions_stage_1(command,person):
	if isAdmin(person):
		person.sendText('====Admin Menu====\n\nList Users: /listusers\nRename User: /renameuser\nList Admins: /listadmins\nSet Admin: /setadmin\nUnset Admin:/unsetadmin\nDelete User: /deleteuser')
from stages.models import *
from users.models import *
from stages.assist import *

def listTheme_1(command, person):
	if isScoreManager(person):
		message = '====Themes====\n\n'
		for theme in Theme.objects.all():
			message += theme.name_cn + '    ' + theme.name_en + '\n'
		person.sendText(message, with_cancel=False)
from stages.models import *
from users.models import *
from stages.assist import *

def deleteTheme_1(command, person):
	if isScoreManager(person):
		functions = []
		for theme in Theme.objects.all():
			addBtnLine(functions,{theme.name_cn + '  ' + theme.name_en : '/'+theme.identifier})
		person.sendText('Which one would you like to delete?', functions)
		person.updateUserProgress('deleteTheme_2')

def deleteTheme_2(command, person):
	if Theme.objects.filter(identifier=command[1:]).count() > 0:
		person.setStorage('deleteTheme', {'identifier':command[1:]})
		theme = Theme.objects.filter(identifier=command[1:])[0]
		functions = []
		addBtnLine(functions, {'Confirm':'/confirm'})
		person.sendText('Them following theme will be deleted upong confirming:\n\nChinese Name: ' +theme.name_cn+ '\nEnglish Name: '+theme.name_en, functions)
		person.stageUp()

def deleteTheme_3(command, person):
	tmp = person.getStorage('deleteTheme')
	theme = Theme.objects.filter(identifier=tmp['identifier'])
	if command == '/confirm':
		if len(theme) > 0 :
			theme[0].delete()
			sendTextToScoreManagers('Following theme has been deleted by '+ person.user_name + ':\n\nChinese Name: ' + theme[0].name_cn + '\nEnglish Name: ' + theme[0].name_en, with_cancel=False)
		else:
			person.sendText('Theme does not exist anymore', with_cancel=False)
		person.popStorage('deleteTheme')
		person.stageEnd()
	else:
		functions = []
		addBtnLine(functions, {'Confirm':'/confirm'})
		person.sendText('Them following theme will be deleted upong confirming:\n\nChinese Name: ' +theme[0].name_cn+ '\nEnglish Name: '+theme[0].name_en, functions)
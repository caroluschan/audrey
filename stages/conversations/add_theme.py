from stages.models import *
from users.models import *
from stages.assist import *

def addTheme_1(command, person):
	if isScoreManager(person):
		person.sendText('Please tell me the Chinese name of the theme')
		person.updateUserProgress('addTheme_2')

def addTheme_2(command, person):
	if command != '/addtheme':
		if Theme.objects.filter(name_cn=command).count() == 0:
			person.setStorage('addTheme', {'name_cn':command})
			person.sendText('Please tell me the English name of the theme')
			person.stageUp()
		else:
			person.sendText('The Chinese name has been used. Please try another')

def addTheme_3(command, person):
	if command[:1] != '/':
		if Theme.objects.filter(name_en=command).count() == 0:
			tmp = person.getStorage('addTheme')
			tmp['name_en'] = command
			person.setStorage('addTheme', tmp)
			functions = []
			addBtnLine(functions, {'Confirm':'/confirm'})
			message = 'Following theme will be created upon confirming.\n\nChinese Name: '+ tmp['name_cn']+'\nEnglish Name: '+ tmp['name_en']
			person.sendText(message, functions)
			person.stageUp()
		else:
			person.sendText('The English name has been used. Please try another')

def addTheme_4(command, person):
	print(command)
	if command == '/confirm':
		tmp = person.getStorage('addTheme')
		newTheme = Theme(identifier=id_generator(Theme), name_cn=tmp['name_cn'], name_en=tmp['name_en'])
		newTheme.save()
		person.popStorage('addTheme')
		person.stageEnd()
		sendTextToScoreManagers('Following theme has been added by '+ person.user_name + ':\n\nChinese Name: ' + tmp['name_cn'] + '\nEnglish Name: ' + tmp['name_en'], with_cancel=False)
	else:
		tmp = person.getStorage('addTheme')
		functions = []
		addBtnLine(functions, {'Confirm':'/confirm'})
		message = 'Following theme will be created upon confirming.\n\nChinese Name: '+ tmp['name_cn']+'\nEnglish Name: '+ tmp['name_en']
		person.sendText(message, functions)

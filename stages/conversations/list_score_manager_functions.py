from users.models import *
from stages.views import *
from stages.models import *

def listScoreManagerFunctions_1(command,person):
	if isScoreManager(person):
		functions = []
		functions.append('List Score Manager:/listscoremanagers\n')
		functions.append('Upload Score:/uploadscore\n')

		message = '===Score Manager Menu===\n\n'

		for function in functions:
			message += function

		person.sendText(message)
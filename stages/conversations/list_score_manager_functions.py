from users.models import *
from stages.views import *
from stages.models import *

def list_score_manager_functions_stage_1(command,person):
	if isScoreManager(person):
		functions = []
		functions.append('List Score Manager:/listscoremanagers\n')

		message = '===Score Manager Menu===\n\n'

		for function in functions:
			message += function

		person.sendText(message)
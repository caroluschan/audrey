from stages.models import *
from users.models import *
from stages.assist import *
from django.conf import settings

#Conversation: get score by code
def get_score_by_code_stage_1(command,person): #command: /songcode[code] | stage_code: songcode_1 | trigger: command[:9] == "/songcode"
	if isApproved(person):
		file = Scores.objects.filter(identifier=command[9:])
		if file:
			person.sendDocument(settings.BASE_DIR+'/scores/'+file[0].file_path, "Here it is my dear :)")
		else:
			person.sendMessage('I\'m sorry :( We do not have score with this code.')
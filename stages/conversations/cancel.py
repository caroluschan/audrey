from stages.models import *
from users.models import *
from stages.assist import *

def cancel_stage_1(command, person): #command: /approve[telegram_id] | stage_code: approve_1 | trigger: command[:8] == "/approve"
	person.stageEnd()
	person.sendText('Your request is been cancelled')
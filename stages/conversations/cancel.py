from stages.models import *
from users.models import *
from stages.assist import *

def cancel_1(command, person): #command: /approve[telegram_id] | stage_code: approve_1 | trigger: command[:8] == "/approve"
	if isApproved(person):
		tmp = person.getStorage()
		stageCode = None
		if person.stage_code is not None:
			stageCode = person.getStageCode()
		if stageCode is not None and stageCode in tmp:
			person.popStorage(stageCode)
		person.stageEnd()
		person.sendText(translate('CANCEL', person.lang), with_cancel=False)
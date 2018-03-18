import string
import random
from stages.models import *
from users.models import *

#######################
####Assist Function####
#######################

def getAdmins():
	return Person.objects.filter(is_admin=True)

def getScoreManagers():
	return Person.objects.filter(is_score_manager=True)

def getScoreManagersNotAdmin():
	return Person.objects.filter(is_score_manager=True, is_admin=False)




def isAdmin(person):
	if person.is_admin:
		return True
	else:
		person.sendText("I'm sorry, only admin can make this request.")

def isScoreManager(person):
	if person.is_score_manager:
		return True
	else:
		person.sendText("I'm sorry, only score manager can make this request.")

def isApproved(person):
	if person.is_approved:
		return True
	else:
		person.sendText(person.user_name+", you will be notified when you signup is approved. If you cannot wait, please contact Admin.")





def findPersonByTelegramId(telegram_id):
	return Person.objects.filter(telegram_id=telegram_id)[0]

def id_generator(model, size=6, chars=string.ascii_uppercase + string.digits):
	identifier = None
	while True:
		identifier =  ''.join(random.choice(chars) for _ in range(size))
		if model.objects.filter(identifier=identifier).count() == 0:
			break
	return identifier




def sendTextToAdmins(message):
	for admin in getAdmins():
			admin.sendText(message)

def sendTextToScoreManagers(message):
	for manager in getScoreManagers():
			manager.sendText(message)

def sendTextToScoreManagersNotAdmin(message):
	for manager in getScoreManagersNotAdmin():
			manager.sendText(message)

def sendTextToAll(message):
	for person in Person.objects.all():
			person.sendText(message)





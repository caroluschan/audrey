# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from stages.models import *
from users.models import *


################################
####Function call for stages####
################################

##########################
###Normal User Function###
##########################

#Conversation: authorization
from conversations.authorization import *

#Conversation: get master list of scores
from conversations.get_master_scores import *

#Conversation: get score by code
from conversations.get_score_by_code import *

#Conversation: get score by song name
from conversations.get_score_by_name import *

#Conversation: get score by lyrics
from conversations.get_score_by_lyrics import *

#Conversation: get lyrics by song name

#Conversation: get lyrics by part of the lyrics

#Conversation: cancel
from conversations.cancel import *

#Conversation: change language
from conversations.change_language import *


#########################
###Admin User Function###
#########################

#Conversation: user approval
from conversations.approve_signup import *
		
#Conversation: list users
from conversations.list_users import *

#Conversation: rename user
from conversations.rename_user import *

#Conversation: list admin users
from conversations.list_admin_users import *

#Conversation: set user as admin
from conversations.set_admin import *

#Conversation: unset admin
from conversations.unset_admin import *

#Conversation: set Score Manager
from conversations.set_score_manager import *

#Conversation: unset Score Manager
from conversations.unset_score_manager import *

#Conversation: list score manager
from conversations.list_score_manager_users import *

#Conversation: delete user
from conversations.delete_user import *

#Conversation: List Admin functions
from conversations.list_admin_functions import *

#Conversation: List Admin functions
from conversations.list_score_manager_functions import *

#Conversation: announcement
from conversations.announcement import *

#Conversation: upload score???
from conversations.upload_score import *
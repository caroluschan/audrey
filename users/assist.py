# -*- coding: utf-8 -*-
import string
import random
import sys
import os
import re
from django.conf import settings

def translate(s, lang='cn', var={}):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	result = translations[s][lang]
	for k, v in var.iteritems():
		tmp = re.split(k, result)
		construct = ''
		for x in range(0,len(tmp)-1):
			construct += tmp[x]
			construct += v
		construct += tmp[len(tmp)-1]
		result = construct
	return result
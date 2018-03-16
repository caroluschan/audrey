import telepot
import time
import json
import urllib2
import urllib
import requests
import sys

def is_ascii(s):
	return all(ord(c) < 128 for c in s)

def handle(msg):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	print("received message")
	#print(msg)
	chat_id = msg['chat']['id']
	command = None
	if 'text' in msg:
		command = msg['text']
		# if is_ascii(command) == False:
		# 	command = unicode(command, "utf-8")
	#elif 'document' in msg:
	headers = {'Content-type': 'application/json'}
	req = urllib2.Request(url='http://127.0.0.1:8000/api/', headers=headers, data=json.dumps({"telegram_id":chat_id, "command":command}))
	response = urllib2.urlopen(req)

bot = telepot.Bot('462615061:AAHqdSi1rMiMpQ9vEpVn3COOkrnSbHrfWm4')
bot.message_loop(handle)
print("Listening")

while 1:
  time.sleep(10)
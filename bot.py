import telepot
import time
import json
import urllib2
import urllib
import requests
import sys
from telepot.loop import MessageLoop

DEBUG_BOT_MODE = False

def is_ascii(s):
	return all(ord(c) < 128 for c in s)

def handle(msg):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	print("received message")
	#print(msg)
	chat_id = msg['chat']['id']
	command = None
	if 'document' in msg:
		command = msg['document']
	elif 'text' in msg:
		command = msg['text']
		# if is_ascii(command) == False:
		# 	command = unicode(command, "utf-8")
	#elif 'document' in msg:
	headers = {'Content-type': 'application/json'}
	req = urllib2.Request(url='http://127.0.0.1:8000/api/', headers=headers, data=json.dumps({"telegram_id":chat_id, "command":command}))
	response = urllib2.urlopen(req)

def handle_callback(msg):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	print("received message")
	#print(msg)
	chat_id = msg['message']['chat']['id']
	command = msg['data']
	query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
	headers = {'Content-type': 'application/json'}
	req = urllib2.Request(url='http://127.0.0.1:8000/api/', headers=headers, data=json.dumps({"telegram_id":chat_id, "command":command, "query_id":query_id}))
	response = urllib2.urlopen(req)

BOT_TOKEN = str('551892984:AAHJFnQhDkwKi8xnrMh_KpDaGkyLSwqD7b4') if DEBUG_BOT_MODE else str('462615061:AAHqdSi1rMiMpQ9vEpVn3COOkrnSbHrfWm4')

bot = telepot.Bot(BOT_TOKEN)
# bot.message_loop(handle)
MessageLoop(bot, {'chat': handle,'callback_query': handle_callback}).run_as_thread()
print("Listening")

while 1:
  time.sleep(10)
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
	bot .sendMessage(chat_id, 'Sorry, I\'m under maintenance now. Will be back soon' )
	
bot = telepot.Bot('462615061:AAHqdSi1rMiMpQ9vEpVn3COOkrnSbHrfWm4')
bot.message_loop(handle)
print("Listening")

while 1:
  time.sleep(10)
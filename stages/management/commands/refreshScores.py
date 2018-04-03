import os
import sys
import json
from stages.assist import *
from stages.models import *
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

class Command(BaseCommand):

	def isEnglish(self, s):
		try:
			s.encode(encoding='utf-8').decode('ascii')
		except UnicodeDecodeError:
			return False
		else:
			return True

	def isDigit(self, s):
		numbers = ['1','2','3','4','5','6','7','8','9','0']
		return True if s in numbers else False

	def strokeChecking(self, s):
		strokes = sorted(os.listdir(settings.BASE_DIR+'/stroke'))
		for stroke in strokes:
			with open(settings.BASE_DIR+'/stroke/'+stroke, 'r') as f:
				data = f.read()
				if s in data:
					return stroke
		return None

	def handle(self, *args, **options):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		connection.cursor()
		connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")
		scores = sorted(os.listdir(settings.BASE_DIR+'/scores'))
		for score in scores:
			if Scores.objects.filter(file_path=score).count() == 0:
				index = None
				if self.isEnglish(score[:1]): 
					index = score[:1]
				else:
					index = score[:3]
				Scores(identifier=id_generator(Scores),file_path=score, index=index).save()
				print(score+' is added to record.')
		for record in Scores.objects.all():
			if record.file_path not in scores:
				print(record.file_path+' is removed from record.')
				record.delete()
		for index in Scores.objects.values('index').distinct():
			if Index.objects.filter(index=index['index']).count() == 0:
				lang = None
				stroke = None
				if self.isDigit(index['index']):
					lang = 'others'
				elif self.isEnglish(index['index']):
					lang = 'en'
				else:
					lang = 'cn'
					stroke = self.strokeChecking(index['index'])
				Index(identifier=id_generator(Index), index=index['index'], language=lang, stroke=stroke).save()
				print('Indexing ' + index['index'])
		for index in Index.objects.all():
			if Scores.objects.filter(index=index.index).count() == 0:
				print('Deindexing ' + index.index)
				index.delete()

			

import os
import sys
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
		Index.objects.all().delete()
		for index in Scores.objects.values('index').distinct():
			Index(identifier=id_generator(Index), index=index['index']).save()
			print('Indexing ' + index['index'])
			

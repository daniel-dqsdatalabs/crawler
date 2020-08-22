#encoding: utf-8

import os, uuid, sys
from scrapy import signals
from scrapy.exceptions import *
from scrapy.utils.project import get_project_settings
from scrapy.exporters import JsonItemExporter,JsonLinesItemExporter
from dqsdatalabs.functions.azdatalake import *

setting = get_project_settings()

class CrawlerPipeline(object):
	
	def __init__(self):
		self.count = 0
		self.file = None
		self.json_exporter = None


	def open_spider(self, spider):
		self.file = open(setting.get('JSON_FILE'), 'w+b')
		self.json_exporter = JsonLinesItemExporter(self.file, encoding='utf-8')
		self.file.write(setting.get('JSON_FIRST_NODE').encode('utf-8'))
		

	def process_item(self, item, spider):
		self.count += 1
		self.json_exporter.export_item(item)
		self.file.write(b',')
		return item

	def close_spider(self, spider):
		if os.stat(setting.get('JSON_FILE')).st_size != 0: 
			# removes the last comma to avoid json mismatch erros
			self.file.seek(-2, os.SEEK_END) # go back 2 characters: \n and ,
			self.file.truncate()
			# end of json
			self.file.write(b']}')
		self.file.close()
		AzDataLake().send_to_datalake()

      
      

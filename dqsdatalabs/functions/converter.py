#encoding: utf-8

from json2parquet import load_json, ingest_data, write_parquet, write_parquet_dataset
from scrapy.utils.project import get_project_settings
from dqsdatalabs.functions import *
import logging

setting = get_project_settings()

class Converter:

	def convert_json_parquet(self):
		try:
			json_file = load_json(setting.get('JSON_FILE'), setting.get('FILE_SCHEMA'))
			write_parquet(json_file, setting.get('PARQUET_FILE'), compression='snappy')
			# enviar o arquivo para o azure data lake
			azure().send_to_datalake()
		except Exception as e:
			logging.log(logging.ERROR, 'Converter.convert_json_parquet => %s' % e.message)

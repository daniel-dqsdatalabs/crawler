#encoding: utf-8

from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from scrapy.utils.project import get_project_settings
from dqsdatalabs.functions import *
import logging 

setting = get_project_settings()


class AzDataLake:

	def send_to_datalake(self):
		try:
			service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format("https", setting.get('STORAGE_ACCOUNT_NAME')), credential=setting.get('STORAGE_ACCOUNT_KEY'))
			file_system_client = service_client.get_file_system_client(file_system=setting.get('AZURE_FILE_SYSTEM'))
			directory_client = file_system_client.get_directory_client(setting.get('DATA_LAKE_DIR'))
   			
			#le o arquivo local
			local_file = open(setting.get('JSON_FILE'), 'r')
			file_contents = local_file.read()
   
			#cria e carrega o arquivo no data lake (local e remoto possuem o mesmo nome)
			file_client = directory_client.create_file(setting.get('JSON_FILE'))
			file_client.append_data(data=file_contents, offset=0, length=len(file_contents))
			file_client.flush_data(len(file_contents))
		except Exception as e:
			logging.log(logging.ERROR, 'AzDataLake.send_to_datalake() => %s' % e.message)



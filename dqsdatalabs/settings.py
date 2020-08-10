#encoding: utf-8

import time, os 
import configparser
import pyarrow as pa 
import scrapy_useragents

###########################
# Private config values
###########################

config_file = configparser.ConfigParser()
config_file.read('../app_config/CRAWLER_FORUM_001.INI')

###########################
# Main configuration
###########################

BOT_NAME = 'dqsdatalabs'
SPIDER_MODULES = ['dqsdatalabs.spiders']
NEWSPIDER_MODULE = 'dqsdatalabs.spiders'

DOWNLOAD_DELAY = 2
ROBOTSTXT_OBEY = False 
FEED_EXPORT_ENCODING = 'utf-8'

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

ITEM_PIPELINES = { 
	'dqsdatalabs.pipelines.CrawlerPipeline' : 0 
}

CRAWLER_NAME = config_file['SCRAPY_CONFIG']['BOT_NAME'] 
START_URLS = config_file['SCRAPY_CONFIG']['START_URLS']
ALLOWED_DOMAINS = config_file['SCRAPY_CONFIG']['ALLOWED_DOMAINS']
JSON_FIRST_NODE = config_file['SCRAPY_CONFIG']['FIRST_NODE_NAME']

###########################
# azure configuration
###########################

STORAGE_ACCOUNT_NAME = config_file['STORAGE_ACCOUNT']['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = config_file['STORAGE_ACCOUNT']['STORAGE_ACCOUNT_KEY']


###########################
# User agent configuration
###########################

# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
# }

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
    'dqsdatalabs.middlewares.CrawlerProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

###########################
# files and paths consts
###########################

LOG_LEVEL = 'INFO'
AZURE_FILE_SYSTEM="raw"
DATA_LAKE_DIR = '{0}/{1}/'.format("dados_crawler", time.strftime("%Y/%m"))
LOG_FILE = '{0}_{1}.{2}'.format("resultado_crawler", time.strftime("%Y%m%d"), "log")
JSON_FILE = '{0}_{1}.{2}'.format("resultado_crawler", time.strftime("%Y%m%d"), "json")
PARQUET_FILE = '{0}_{1}.{2}'.format("resultado_crawler", time.strftime("%Y%m%d"), "parquet")


###########################
# parquet schema
###########################

FILE_SCHEMA = pa.schema([
	pa.field('page_url', pa.string()),
	pa.field('page_category', pa.string()),
	pa.field('page_category_text', pa.string()),
	pa.field('question_link', pa.string()),
	pa.field('question_title', pa.string()),
	pa.field('question_username', pa.string()),
	pa.field('question_datetime', pa.string()),
	pa.field('question_comments_count', pa.string()),
	pa.field('question_views_count', pa.string()),
	pa.field('question_text', pa.string()),
	pa.field('question_answers', pa.list_(pa.string()))
])

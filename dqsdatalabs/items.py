#encoding: utf-8

import scrapy

class CrawlerItem(scrapy.Item):
	page_url = scrapy.Field() 
	page_category = scrapy.Field() 
	page_category_text = scrapy.Field() 
	question_link = scrapy.Field() 
	question_title = scrapy.Field() 
	question_username = scrapy.Field() 
	question_datetime = scrapy.Field() 
	question_comments_count = scrapy.Field() 
	question_views_count = scrapy.Field() 
	question_text = scrapy.Field() 
	question_answers = scrapy.Field() 


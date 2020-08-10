#encoding: utf-8

import time
import scrapy
import logging
import numpy as np 
from bs4 import BeautifulSoup
from dqsdatalabs.items import *
from dqsdatalabs.functions.converter import *
from scrapy.utils.project import get_project_settings

seeting = get_project_settings()

class Forum001Spider(scrapy.Spider):
    
	start_urls = []
	allowed_domains = []

	name = seeting.get('CRAWLER_NAME')
	allowed_domains.append(seeting.get("ALLOWED_DOMAINS"))
	start_urls.append(seeting.get("START_URLS"))
 
	def parse(self, response):
		logging.log(logging.INFO, 'User-Agent do Request: %s' % response.request.headers['User-Agent'])
		items = response.xpath('//a[contains(@class,"ItemLink")]').extract()

		# percorre as categorias e extrai os respectivos links
		for item in items:
			soup = BeautifulSoup(item,'html.parser')
			category = soup.find('span').contents[0]
			page_url = soup.findAll('a', {'class': 'ItemLink'})[0]['href']

			try:
				yield scrapy.Request(page_url, callback=self.process_url_level_one, meta={"page_url": page_url, "page_category": category})
			except Exception as e:
				logging.log(logging.ERROR,'{%s} : {%s}' %page_url, e.message)
				pass 

	def process_url_level_one(self, response):
		page_args = {}
		subpage_args = {}  
		page_url = response.meta["page_url"]
		page_category = response.meta["page_category"]
		page_category_text = response.xpath('//p[@class="post-ttl-p"]/text()').extract_first()

		page_args = {
			'page_url' : page_url,
			'page_category': page_category, 
			'page_category_text': page_category_text
		}

		# pega as perguntas
		for row in response.xpath('//*[@class="DataTable DiscussionsTable"]//tbody/tr'):
			question_link = row.xpath('td[1]/div/a/@href').extract_first(), 
			question_title = row.xpath('td[1]/div/a/text()').extract_first(),
			question_username = row.xpath('td[2]/div/span/text()').extract_first(),
			question_datetime = row.xpath('td[2]/div/div/span/time/@datetime').extract_first(),
			question_comments_count = row.xpath('td[3]/span/span/text()').extract_first(),
			question_views_count = row.xpath('td[4]/div/span/text()').extract_first()
			
			question_args = {
				'question_link': question_link, 
				'question_title': question_title,
				'question_username': question_username,
				'question_datetime': question_datetime,
				'question_comments_count': question_comments_count,
				'question_views_count': question_views_count
			}

			try:
				yield scrapy.Request(question_link[0], callback=self.process_url_level_two, meta={'page_args': page_args, 'question_args': question_args})
			except Exception as e:
				logging.log(logging.ERROR,'{%s} : {%s}' %question_link[0], e.message)
				pass 
				
		# paginacao
		try:
			next_page_url = response.xpath('//*[contains(text(), "»")]/@href').extract_first()
			yield scrapy.Request(next_page_url)
		except:
			pass 

	def process_url_level_two(self, response):
		item = CrawlerItem()
		item['page_url'] = response.meta["page_args"]["page_url"]
		item['page_category'] = response.meta["page_args"]["page_category"]
		item['page_category_text'] = response.meta["page_args"]["page_category_text"]
		item['question_link'] = response.meta["question_args"]["question_link"]
		item['question_title'] = response.meta["question_args"]["question_title"]
		item['question_username'] = response.meta["question_args"]["question_username"]
		item['question_datetime'] = response.meta["question_args"]["question_datetime"]
		item['question_comments_count'] = response.meta["question_args"]["question_comments_count"]
		item['question_views_count'] = response.meta["question_args"]["question_views_count"]
		item['question_text'] = ''.join(response.xpath('(//div[@class="Message userContent"])[1]/text()').extract())
		item['question_answers'] = {}
  
		data = response.xpath('(//div[@class="Message userContent"])')
		for i in range(len(data)):
			var = '(//div[@class="Message userContent"])[$]/text()'.replace("$", str(i)) 
			if i != 1: item['question_answers']['question_answer_' + str(i)] = ''.join(response.xpath(var).extract()) 

		return item


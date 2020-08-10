#encoding: utf-8

import logging 
import proxyscrape
from scrapy import signals

class CrawlerSpiderMiddleware(object):
	
	@classmethod
	def from_crawler(cls, crawler):
		s = cls()
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s

	def process_spider_input(self, response, spider):
		return None

	def process_spider_output(self, response, result, spider):
		for i in result:
			yield i

	def process_spider_exception(self, response, exception, spider):
		pass

	def process_start_requests(self, start_requests, spider):
		for r in start_requests:
			yield r

	def spider_opened(self, spider):
		logging.log(logging.INFO, 'Spider opened: %s' % spider.name)


class CrawlerDownloaderMiddleware(object):
	
	@classmethod
	def from_crawler(cls, crawler):
		s = cls()
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s

	def process_request(self, request, spider):
		return None

	def process_response(self, request, response, spider):
		return response

	def process_exception(self, request, exception, spider):
		pass

	def spider_opened(self, spider):
		logging.log(logging.INFO, 'Spider opened: %s' % spider.name)
  
  
class CrawlerProxyMiddleware(object):

	def __init__(self):
		self.collector = proxyscrape.create_collector('proxy-collector', 'http')
		self.collector.apply_filter({'country': 'brazil'})
	
	def process_request(self, request, spider):
		proxy = self.get_random_proxy() 
		request.meta['proxy'] = proxy 
		logging.log(logging.INFO, 'REQUEST IP [%s]' % proxy)
		return None 
		
	def process_response(self, request, response, spider):
		if response.status != 200:
			proxy = self.get_random_proxy() 
			logging.log(logging.INFO, 'RESPONSE IP [%s]' % proxy)
			return request 
		return response 

	def get_random_proxy(self):
		self.collector.refresh_proxies(force = True)
		proxy = self.collector.get_proxy()
		return '{0}:{1}'.format(proxy[0], proxy[1])
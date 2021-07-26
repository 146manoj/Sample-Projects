# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class AmazonPipeline(object):

	def __init__(self):
		self.asin_seen = set()
		
	def process_item(self, item, spider):
		if item['ASIN'] in self.asin_seen:
			raise DropItem('Duplicate item found: %s' % item['ASIN'])
		else:
			self.asin_seen.add(item['ASIN'])
		return item
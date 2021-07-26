# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
import re

from BIGBASKET_SEARCH import settings
from scrapy import signals
from pydispatch import dispatcher
import csv
from scrapy.utils.response import open_in_browser
from datetime import datetime, timedelta

from scraper_api import ScraperAPIClient
client = ScraperAPIClient('APIKEY')

class BigbasketSpider(scrapy.Spider):
	name = 'bigbasket'
	start_urls = ['http://api.scraperapi.com/?api_key=APIKEY&url=https://www.bigbasket.com']
	
	CSV_TITLE = [
				"Product_url", "TimeStamp", "Retailer", "Search_Term", "Sponsored_Organic_Flag", "Search_Page", 
				"Search_Rank", "Product_Name", "Manufacturer", "Ratings", "Nratings", "MRP", 
				"Selling_Price", "Discount", "SNS", "Delivery_comments", "Seller_Comments", 
				"Stock_Information", "EAN/ASIN/ID", "Additional_Comments"
			]

	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		self.csv_file = open('RESULT.csv','w', newline='')
		self.csv_wr = csv.writer(self.csv_file, quoting=csv.QUOTE_ALL)
		self.csv_wr.writerow(self.CSV_TITLE)
		
		File = open('Input_links.csv', 'r')
		Reader = csv.reader(File)
		self.Keywords = list(Reader)
		self.counts = len(self.Keywords)

	def spider_closed(self, spider):
		self.csv_file.close()
		
	def start_requests(self):
		for i in range(self.counts):
			Keyword = self.Keywords[i][0]
			URL = 'https://www.bigbasket.com/ps/?q=' + str(Keyword) + '#!page=1'
			rq = scrapy.Request(client.scrapyGet(URL, headers={"X-MyHeader": "123"}), callback=self.parse)
			rq.meta['Keyword'] = Keyword
			yield rq
			
	def parse(self, response):
		Keyword = response.meta['Keyword']
		Search_Page = "".join(re.findall('(\d+)$',str(response.url))).strip()
		TimeStamp = datetime.now().strftime("%d/%m/%Y") + ' ' + datetime.now().strftime("%H:%M:%S")
		Retailer = "Bigbasket"
		Search_Term = Keyword
		Manufacturer = "NA"#sel.xpath('/text()').extract()
		for sel, count in zip(response.xpath('//ul/li[@qa="product"]'), range(len(response.xpath('//ul/li[@qa="product"]')))):
			Sponsored_Organic_Flag = "NA"#.join(sel.xpath('.//div[@class="a-row a-spacing-micro"]/span/text()').extract()).strip()
			Search_Rank = count
			Product_Name = "".join(sel.xpath('./div[@qa="product_name"]/span/a/span[2]/text()').extract()).strip()
			Product_url = "".join(sel.xpath('./div[@qa="product_name"]/span/a/@href').extract()).strip()
			Product_url = "https://www.bigbasket.com" + Product_url
			Ratings = "NA"#.join(sel.xpath('.//div[@class="a-row a-size-small"]/span[1]/@aria-label').extract()).strip()
			Nratings = "NA"#.join(sel.xpath('.//div[@class="a-row a-size-small"]/span[2]/@aria-label').extract()).strip()
			MRP = "".join(sel.xpath('.//div[@class="Rate_count_low"]/span/text()[normalize-space()]').extract()).strip()
			Selling_Price = "".join(sel.xpath('.//div[@qa="priceRP"]/text()').extract()).strip()
			Discount = "0"#.join(sel.xpath('.//div[@class="a-row a-size-base a-color-base"]/div/span[2]/text()').re('\D+(\d+.*)')).strip()
			SNS = "NA"#.join(sel.xpath('.//div[@class="a-row a-size-base a-color-secondary"]/div/span/text()').extract()).strip()
			Delivery_comments = "".join(sel.xpath('.//div[@class="uiv2-rate-count-text delivery-slot-label"]/label/text()').extract()).strip()
			Seller_Comments = "NA"#.join(sel.xpath('.//div[@class="a-row a-size-base a-color-secondary s-align-children-center"]/div[@class="a-row"]/span/span/text()').re('(Ful.*)')).strip()
			Stock_Information = "NA"#sel.xpath('/text()').extract()
			EAN_ASIN_ID = "".join(re.findall('pd\/(\d+)\/',str(Product_url))).strip()
			Additional_Comments = "NA"#sel.xpath('/text()').extract()
			
			data = [
				Product_url,
				TimeStamp,
				Retailer,
				Search_Term,
				Sponsored_Organic_Flag,
				Search_Page,
				Search_Rank,
				Product_Name,
				Manufacturer,
				Ratings,
				Nratings,
				MRP,
				Selling_Price,
				Discount,
				SNS,
				Delivery_comments,
				Seller_Comments,
				Stock_Information,
				EAN_ASIN_ID,
				Additional_Comments,
				]
			print ('Saving to Results Sheet => ', data)
			self.csv_wr.writerow(data)
			
			next_page = response.xpath('//*[contains(@id,"products-page")]/text()').re_first('\d+')
			if next_page:
				next_url = 'https://www.bigbasket.com/ps/?q=' + str(Keyword) + '#!page=' + next_page
				print ('Next_Page =>', next_url)
				rq = scrapy.Request(next_url, callback=self.parse)
				# rq.meta['Retailer'] = Retailer
				rq.meta['Keyword'] = Keyword
				# rq.meta['Manufacturer'] = Manufacturer
				# rq.meta['Stock_Information'] = Stock_Information
				# rq.meta['Additional_Comments'] = Additional_Comments
				yield rq
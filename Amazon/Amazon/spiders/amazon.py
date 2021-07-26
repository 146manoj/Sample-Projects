# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
import re

from Amazon import settings
from scrapy import signals
from pydispatch import dispatcher
import csv
from scrapy.utils.response import open_in_browser
from datetime import datetime, timedelta

from scraper_api import ScraperAPIClient
client = ScraperAPIClient('API KEY')

class AmazonSpider(scrapy.Spider):
	name = "amazon"
	start_urls = ['http://api.scraperapi.com/?api_key=APIKEY&url=https://www.amazon.in/gp/bestsellers/hpc/&session_number=123']

	CSV_TITLE = [
				"Product_URL", "MRP", "Sale Price", "Offer Price", "Promotion (Discount)", 
				"Offers (includes lightening deals, BOGO, cashback etc.)", "Seller list with price across sellers", 
				"Buy Box (seller listed on the product page)", "Inventory or Stock remaining (if available)", "Ratings", 
				"Reviews (including historical reviews dump with date stamp)", "Review features (as decided by retailer)", 
				"Product Name", "Product images", "Product images count", "Product Description", 
				"Product details (manufacturer supplied with images)", 
				"Platform sold on (pantry, dotcom, subscribe & save)", 
				"ASIN number (or respective stock identification number on other retailers)", 
				"Product dimension", "Item model number", "Date first available on amazon/retailer", 
				"Amazon Best seller rank 1", "Amazon Best seller rank 2", "Amazon Best seller rank 3", 
				"Amazon Best seller rank 4", "Amazon Best seller rank 2", "Popularity index/rank (for other retailers)", 
				"Pack size (if available or it should be available on the product name/desc)", "Other sponsored products ", 
				"Typical customer questions asked with responses"
			]

	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		self.csv_file = open('RESULT.csv','w', newline='')
		self.csv_wr = csv.writer(self.csv_file, quoting=csv.QUOTE_ALL)
		self.csv_wr.writerow(self.CSV_TITLE)
		
		File = open('Input_links.csv', 'r')
		Reader = csv.reader(File)
		self.Links = list(Reader)
		self.counts = len(self.Links)

	def spider_closed(self, spider):
		self.csv_file.close()
		
	def start_requests(self):
		for i in range(self.counts):
			Link = self.Links[i][0]
			yield scrapy.Request(client.scrapyGet(Link, render=True), callback=self.parse)
			
		next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
		if next_page:
			yield scrapy.Request(client.scrapyGet(Link, render=True), callback=self.parse)
			
	def parse(self, response):
		for list_urls in response.xpath('//div[contains(@class, "s-result-list s-search-results sg-row")]//div/h2/a/@href').extract():
			list_url = 'https://www.amazon.in' + list_urls
			rq = scrapy.Request(client.scrapyGet(list_url, render=True), callback=self.parse_prod)
			yield rq
			
	def parse_prod(self, response):
		Product_URL = response.url
		MRP = "".join(response.xpath('//span[@class="priceBlockStrikePriceString a-text-strike"]/text()').re('([\d\.\,]+)')).strip()
		Sale_Price = "".join(response.xpath('//span[@class="a-size-medium a-color-price priceBlockBuyingPriceString"]/text()').re('([\d\.\,]+)')).strip()
		Offer_Price = "NA"#.join(response.xpath('/text()').extract()).strip()
		Promotion = "".join(response.xpath('//td[@class="a-span12 a-color-price a-size-base priceBlockSavingsString"]/text()').re('([\d\.\,\(\)\%]+)')).strip()
		Offers = "NA"#.join(response.xpath('/text()').extract()).strip()
		Seller_list_with_price_across_sellers = "".join(response.xpath('/text()').extract()).strip()
		Buy_Box = "".join(response.xpath('//div[@id="merchant-info"]//text()').extract()).strip()
		if b'In stock' in response.body:
			Inventory_or_Stock_remaining = 'In Stock'
		else:
			Inventory_or_Stock_remaining = ''
		Ratings = "".join(response.xpath('//span[@data-hook="rating-out-of-text"]/text()').extract()).strip()
		Reviews = "".join(response.xpath('/text()').extract()).strip()
		Review_features = "".join(response.xpath('/text()').extract()).strip()
		Product_Name = "".join(response.xpath('//span[@id="productTitle"]/text()').extract()).strip()
		Product_images = "".join(response.xpath('//img[contains(@src,"SS40")]/@src').extract()).strip()
		Product_images_count = len(response.xpath('//img[contains(@src,"SS40")]/@src').extract())
		Product_Description = "".join(response.xpath('//div[@id="productDescription"]/p/text()').extract()).strip()
		Product_details_ = ""#.join(response.xpath('/text()').extract()).strip()
		Platform_sold_on = ""#.join(response.xpath('/text()').extract()).strip()
		ASIN_number = re.findall('dp\D(\w+)', str(response.url))
		Product_dimension = "".join(response.xpath('//td[contains(.," Dimensions")]/following-sibling::td[1]/text() | //b[contains(.," Dimensions")]/following-sibling::text()[1]').extract()).strip()
		Item_model_number = "".join(response.xpath('//td[contains(.,"Item model number")]/following-sibling::td[1]/text() | //b[contains(.,"Item part number")]/following-sibling::text()[1]').extract()).strip()
		Date_first_available_on_amazon_or_retailer = "".join(response.xpath('//td[contains(.,"Date First Available")]/following-sibling::td[1]/text() | //b[contains(.,"Date first available")]/following-sibling::text()[1]').extract()).strip()
		Amazon_Best_seller_rank_1 = "".join(response.xpath('//td[contains(.,"Amazon Bestsellers Rank")]/following-sibling::td[1]/text() | //b[contains(.,"Amazon Bestsellers Rank")]/following-sibling::text()[1]').extract()).strip()
		Amazon_Best_seller_rank_2 = "NA"#.join(response.xpath('//li[@class="zg_hrsr_item"]//text()').extract()).strip()
		Amazon_Best_seller_rank_3 = "NA"#.join(response.xpath('/text()').extract()).strip()
		Amazon_Best_seller_rank_4 = "NA"#.join(response.xpath('/text()').extract()).strip()
		Amazon_Best_seller_rank_2 = "NA"#.join(response.xpath('/text()').extract()).strip()
		Popularity_index_or_rank = "NA"#.join(response.xpath('/text()').extract()).strip()
		Pack_size = "".join(response.xpath('//*[@id="prodDetails"]/div[1]/text() | //*[@id="detail_bullets_id"]/table//tr/td/div[1]/text()').extract()).strip()
		Other_sponsored_products = ""#.join(response.xpath('/text()').extract()).strip()
		Typical_customer_questions_asked_with_responses = ""#.join(response.xpath('/text()').extract()).strip()
		data = [
			Product_URL,
			MRP,
			Sale_Price,
			Offer_Price,
			Promotion,
			Offers,
			Seller_list_with_price_across_sellers,
			Buy_Box,
			Inventory_or_Stock_remaining,
			Ratings,
			Reviews,
			Review_features,
			Product_Name,
			Product_images,
			Product_images_count,
			Product_Description,
			Product_details_,
			Platform_sold_on,
			ASIN_number,
			Product_dimension,
			Item_model_number,
			Date_first_available_on_amazon_or_retailer,
			Amazon_Best_seller_rank_1,
			Amazon_Best_seller_rank_2,
			Amazon_Best_seller_rank_3,
			Amazon_Best_seller_rank_4,
			Amazon_Best_seller_rank_2,
			Popularity_index_or_rank,
			Pack_size,
			Other_sponsored_products,
			Typical_customer_questions_asked_with_responses,
			]
		print ('Saving to Results Sheet => ', data)
		self.csv_wr.writerow(data)
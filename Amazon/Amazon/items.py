# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    Title = scrapy.Field()
    Brand = scrapy.Field()
    Best_Seller_Rank = scrapy.Field()
    Total_Sellers_or_Offers = scrapy.Field()
    Buy_Box_Price = scrapy.Field()
    Weight_and_Dimensions = scrapy.Field()
    FBA = scrapy.Field()
    No_of_reviews = scrapy.Field()
    ASIN = scrapy.Field()
    Page_No = scrapy.Field()
    Link = scrapy.Field()
    sold_by = scrapy.Field()
# import base64

# class ProxyMiddleware(object):
    # def process_request(self, request, spider):
        # request.meta['proxy'] = "http://65.74.171.129:80"

        
        
import base64
from scrapy.http import Request
from scrapy.selector import Selector
import requests
from lxml import html
import json

proxy='65513da9eef08b3a591e789b2c4efee2'
class ProxyMiddleware(object):
	def process_request(self, request, spider):
		proxy_host = "http://api.scraperapi.com/?api_key="
		proxy_port = "8010"
		proxy_auth = proxy+":" # Make sure to include ':' at the end
		proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
			  "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}
		# print proxies  
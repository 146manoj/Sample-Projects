# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.utils.response import open_in_browser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import csv
from selenium.webdriver.common.action_chains import ActionChains
from scrapy import signals
from pydispatch import dispatcher


CSV_TITLE = [
		"Name of Establishments", "Website", "address", "Phone", "Ratings"
		]

driver = webdriver.Chrome(executable_path='chromedriver.exe')
csv_file = open("Results.csv", "w", newline='', encoding='utf-8')
csv_wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
csv_wr.writerow(CSV_TITLE)
driver.get("https://www.google.com/maps")
wait = WebDriverWait(driver, 1200)


File = open('Input_links.csv', 'r')
Reader = csv.reader(File)
Names = list(Reader)
counts = len(Names)

def parse():
	for i in range(counts):
		Location = Names[i][0] + " in california"
		if Location:
			search_xpath = '//*[@id="searchboxinput"]'
			search = wait.until(EC.presence_of_element_located((By.XPATH, search_xpath)))
			search.clear()
			search.send_keys(Location + Keys.ENTER)
			parse_data()
		else:
			csv_file.close()

def parse_data():
	time.sleep(4)
	wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="section-hero-header-title-top-container"] | //div[@role="region"]/div[@data-result-index="1"] | //div[@class="section-result-content"] | //div[@class="tYZdQJV9xeh__title gm2-subtitle-alt-2"] | //span[contains(.,"Make sure your search is spelled correctly.")]')))
	wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="section-hero-header-title-top-container"] | //div[@role="region"]/div[@data-result-index="1"] | //div[@class="section-result-content"] | //div[@class="tYZdQJV9xeh__title gm2-subtitle-alt-2"] | //span[contains(.,"Make sure your search is spelled correctly.")]')))
	if 'section-layout section-scrollbox scrollable-y scrollable-show section-layout-flex-vertical' in driver.page_source:
		time.sleep(2)
		name_link = '//div[@class="section-result-content"] | //div[@class="tYZdQJV9xeh__title gm2-subtitle-alt-2"]'
		name_link = wait.until(EC.presence_of_element_located((By.XPATH, name_link)))
		name_link = name_link.click()
		parse_results()
	elif 'Partial match' in driver.page_source:
		pass
	else:
		parse_results()
		
def parse_results():
	time.sleep(2)
	try:
		Name = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]')
		Name = Name.get_attribute('textContent')
	except:
		Name = ""
	try:
		Website = driver.find_element_by_xpath('//img[contains(@src,"public_gm_blue")]/following::div[1]/div[1]').get_attribute('textContent')
	except:
		Website = ""
	try:
		Address = driver.find_element_by_xpath('//img[contains(@src,"place_gm_blue")]/following::div[1]/div[1]').get_attribute('textContent')
	except:
		Address = ""
	try:
		Phone = driver.find_element_by_xpath('//img[contains(@src,"phone_gm_blue")]/following::div[1]/div[1]').get_attribute('textContent')
	except:
		Phone = ""
	try:
		rating = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span').get_attribute('textContent')
	except:
		rating = ""
	data = [
		Name,
		Website,
		Address,
		Phone,
		rating,
		]
	print ('Saving to Results Sheet => ', data)
	csv_wr.writerow(data)
	csv_file.flush()

parse()
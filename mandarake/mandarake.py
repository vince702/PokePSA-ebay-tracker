import os
import copy
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import json # for testing

class card:
    def __init__(self):
        self.name = name
        self.price = price
    
def check_if_new():
    return [card()]

def import_saved():
    return True

def initDriver():
    # get initial html
    driverpath = os.path.realpath(r'drivers/chromedriver')
    chrome_options = Options()  
    # chrome_options.add_argument("--headless")  

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get('https://order.mandarake.co.jp/order/listPage/list?upToMinutes=360&layout=2&sort=price&soldOut=1&categoryCode=0602&lang=en') # base webpage

    return driver

def get_above_5000_yen(driver):
    to_check = []
    card_list = driver.find_element_by_class_name("infolist")
    for card in card_list.find_elements_by_class_name("block"):
        price = card.find_element_by_class_name("price").find_element_by_tag_name("p").get_attribute('innerHTML')
        price = price.replace(' yen', '')
        price = price.replace(',', '')
        if float(price) > 5000:
            to_check.append(card.find_element_by_class_name('title'))
    return to_check

driver = initDriver()
search_cards = get_above_5000_yen(driver)
print(search_cards)
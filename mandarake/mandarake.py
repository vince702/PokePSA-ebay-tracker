import os
import copy
import re
import csv

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
    # driver.get('https://order.mandarake.co.jp/order/listPage/list?upToMinutes=360&layout=2&sort=price&soldOut=1&categoryCode=0602&lang=en') # base webpage
    driver.get('https://order.mandarake.co.jp/order/listPage/list?upToMinutes=720&layout=2&sort=price&soldOut=1&categoryCode=0602&lang=en')
    return driver

def get_above_5000_yen(driver):
    to_check = []
    card_list = driver.find_element_by_class_name("infolist")
    for card in card_list.find_elements_by_class_name("block"):
        price = card.find_element_by_class_name("price").find_element_by_tag_name("p").get_attribute('innerHTML')
        price = price.replace(' yen', '')
        price = price.replace(',', '')
        if float(price) > 5000:
        # if float(price) > 1000:
            to_check.append(remove_spaces(card.find_element_by_class_name('title').find_element_by_tag_name("a").get_attribute('innerHTML')))
    return to_check

def remove_spaces(inp):
    return "".join(inp.split())

def read_from_csv():
    out = []
    f=open("saved.csv")
    for row in csv.reader(f):
        # print('row', row[0])
        out.append(row[0])
    return out

driver = initDriver()
search_cards = get_above_5000_yen(driver)
# print('search cards', search_cards)

content = read_from_csv()
# print('content', content)

def diff(li1, li2): 
    return (list(set(li1) - set(li2)))

import os

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

# print(diff(search_cards, content)) 
the_list = diff(search_cards, content)
# print(the_list)

if len(the_list) > 0:
    # print('notify user')
    notify("new card", the_list)


with open('saved.csv', 'a') as file_handler:
    for item in the_list:
        # print(item)
        file_handler.write("{}\n".format(item))

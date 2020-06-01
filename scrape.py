import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

import json # for testing

def initDriver():
    # get initial html
    driverpath = os.path.realpath(r'drivers/chromedriver')
    chrome_options = Options()  
    # chrome_options.add_argument("--headless")  

    driver = webdriver.Chrome(driverpath, options=chrome_options)
    driver.get('https://www.psacard.com/pop/tcg-cards/156940') # base webpage

    return driver

# base page
# https://www.psacard.com/pop/tcg-cards/156940
def get_tcg_years():
    return 0

# filter href links for set names with 'Pokemon' in it
# https://www.psacard.com/pop/tcg-cards/1993/156957
def pokemon_cards_by_year():
    return 0

# get card_no, name, sub_name (ex. edition, holo, etc.)
def card_definition(set):
    return 0

driver = initDriver()
driver.quit()
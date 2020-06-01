import os
import copy

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

import json # for testing

data = []

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
def get_tcg_years(driver):
    grid = driver.find_element_by_id('years-grid')
    table = grid.find_element_by_tag_name('tbody')
    rows = table.find_elements_by_class_name('even') + table.find_elements_by_class_name('odd')

    years = []
    ind = 0
    for row in rows:
        if 'totals' in row.get_attribute('class').split(): # remove label row
            rows.pop(ind)
        else:
            year_elem = row.find_element_by_tag_name('a')
            year = year_elem.get_attribute('innerHTML')
            link = year_elem.get_attribute('href')
            years.append({
                'year': year,
                'link': link
            })
        ind += 1

    return years

# filter href links for set names with 'Pokemon' in it
# https://www.psacard.com/pop/tcg-cards/1993/156957
def pokemon_cards_by_year(driver, link):
    driver.get(link) # navigate to page

    grid = driver.find_element_by_id('pop-grid')
    table = grid.find_element_by_tag_name('tbody')
    rows = table.find_elements_by_class_name('even') + table.find_elements_by_class_name('odd')

    links = []
    ind = 0
    for row in rows:
        if 'totals' in row.get_attribute('class').split(): # remove label row
            rows.pop(ind)
        else:
            elem = row.find_element_by_tag_name('a')
            name = elem.get_attribute('innerHTML')
            if 'Pokemon' in name:
                link = elem.get_attribute('href')
                links.append({
                    'name': name,
                    'link': link
                })

    return links

# get card_no, name, sub_name (ex. edition, holo, etc.)
def definition(driver, card):
    driver.get(card) # navigate to page
    return {
        'head': 'asdf',
        'sub': 'asdf'
    }

driver = initDriver()
res = []
for year in get_tcg_years(driver):
    cards = pokemon_cards_by_year(driver, year['link'])
    for card in cards:
        card_definition = definition(driver, card['link'])
        print(year['year'], card['name'], card_definition['head'], card_definition['sub'])
        card = {
            'year' : year['year'], 
            'card' : card['name'],
            'name' : card_definition['head'],
            'sub'  : card_definition['sub']
        }
        res.append(card)
        print(json.dumps(card, indent=2))
        print('\n')

print('result')
print(res)

driver.quit()
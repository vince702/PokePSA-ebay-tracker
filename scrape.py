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
def get_tcg_years(driver):
    grid = driver.find_element_by_id('years-grid')
    table = grid.find_element_by_tag_name('tbody')
    rows = table.find_elements_by_class_name('even') + table.find_elements_by_class_name('odd')

    years = {}
    ind = 0
    for row in rows:
        if 'totals' in row.get_attribute('class').split(): # remove label row
            rows.pop(ind)
        else:
            year_elem = row.find_element_by_tag_name('a')
            year = year_elem.get_attribute('innerHTML')
            link = year_elem.get_attribute('href')
            years[year] = link
        ind += 1

    return years

# filter href links for set names with 'Pokemon' in it
# https://www.psacard.com/pop/tcg-cards/1993/156957
def pokemon_cards_by_year(driver, link):
    driver.get(link) # navigate to page

    grid = driver.find_element_by_id('pop-grid')
    table = grid.find_element_by_tag_name('tbody')
    rows = table.find_elements_by_class_name('even') + table.find_elements_by_class_name('odd')

    links = {}
    ind = 0
    for row in rows:
        if 'totals' in row.get_attribute('class').split(): # remove label row
            rows.pop(ind)
        else:
            elem = row.find_element_by_tag_name('a')
            name = elem.get_attribute('innerHTML')
            if 'Pokemon' in name:
                link = elem.get_attribute('href')
                links[name] = link

    return links

# get card_no, name, sub_name (ex. edition, holo, etc.)
def card_definition(set):
    return 0

driver = initDriver()
years = get_tcg_years(driver)
for year, link in years.items():
    cards = pokemon_cards_by_year(driver, link)
    print(year, cards)

driver.quit()
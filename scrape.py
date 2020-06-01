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

data = []

def remove_spaces(inp):
    return "".join(inp.split())

def initDriver():
    # get initial html
    driverpath = os.path.realpath(r'drivers/chromedriver')
    chrome_options = Options()  
    # chrome_options.add_argument("--headless")  

    driver = webdriver.Chrome(driverpath, options=chrome_options)
    driver.get('https://www.psacard.com/pop/tcg-cards/156940') # base webpage

    return driver

def click_expansion(driver, link, wait_until_exists):
    # click expand button
    driver.get(link)

    # wait until detaillayout is expanded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
        By.ID, wait_until_exists)))

    # extraction logic
    return driver.find_element_by_id(wait_until_exists)

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
    # driver.get(link) # navigate to page
    click_expansion(driver, link, 'pop-grid') # wait til pop-grid exists in case if cloudflare stops

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
                    'series': name,
                    'link': link
                })

    return links

# get card_no, name, sub_name (ex. edition, holo, etc.)
def get_definition(driver, link):
    # driver.get(card) # navigate to page
    grid = click_expansion(driver, link, 'DataTables_Table_0_wrapper') # wait til pop-grid exists in case if cloudflare stops
    table = grid.find_element_by_tag_name('tbody')
    rows = table.find_elements_by_class_name('even') + table.find_elements_by_class_name('odd')
    
    def parse_name(wrapper): # TODO
        source = wrapper.get_attribute('innerHTML')
        # text = wrapper.find_element_by_xpath("//strong").get_attribute('text')
        # print(text)
        # source = source.replace(text, '').get_attribute('innerHTML')

        res = []
        remove_tags = re.sub('<[^>]+>', '', source)
        split_elem = re.split("(\s+)", remove_tags)
        i = 0
        for elem in remove_tags.replace('Shop', '').split('\n'):
            # print(remove_spaces(elem))
            # print(remove_spaces(elem) == '')
            if remove_spaces(elem) != '':
                res.append(elem)
                # print(split_elem)
            i += 1
        # print(res)
        return res

    details = []
    ind = 0
    for row in rows:
        if 'totals' in row.get_attribute('class').split(): # remove label row
            rows.pop(ind)
        else:
            data = row.find_elements_by_tag_name('td')
            card_no = data[0].get_attribute('innerHTML')
            card_name_wrapper = data[1]
            parsed = parse_name(card_name_wrapper) # ADD as header, subheader
            if len(parsed) > 1: # has subheader
            # if (subheader):
                details.append({
                    'card_no': card_no,
                    'head': remove_spaces(parsed[0]),
                    'sub': remove_spaces(parsed[1])
                })
            else:
                details.append({
                    'card_no': card_no,
                    'head': remove_spaces(parsed[0]),
                })

    return details

driver = initDriver()
res = []
for year in get_tcg_years(driver):
    cards = pokemon_cards_by_year(driver, year['link'])
    for card in cards:
        card_definition = get_definition(driver, card['link'])
        # print(year['year'], card['series'], card_definition['head'], card_definition['sub'])
        for definition in card_definition:
            card = {
                'year' : year['year'], 
                'series' : card['series'],
                'card_no': remove_spaces(definition['card_no']),
                'name' : definition['head'],
            }
            try:
                card['sub'] = definition['sub']
            except:
                print('unlucky')

            res.append(card)
            # print(json.dumps(card, indent=2))
            # print('\n')

print('result')
print(res)

driver.quit()
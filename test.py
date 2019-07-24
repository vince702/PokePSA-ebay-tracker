import datetime
import sys

import ssl
import urllib.request
from bs4 import BeautifulSoup

from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import ebaysdk.shopping
import os
import re

os.environ.setdefault("EBAY_YAML", "ebay.yaml")


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
psa_url = "https://www.psacard.com/cert/"
headers={'User-Agent':user_agent,} 
ssl._create_default_https_context = ssl._create_unverified_context

from PIL import Image

from pytesseract import image_to_string


im = urllib.request.urlopen('https://i.ebayimg.com/00/s/MTYwMFgxMjAw/z/WgYAAOSwrpNdFVM7/$_57.JPG?set_id=8800005007')



text = re.findall(r'[0-9]{8}',image_to_string(Image.open(im)))
print(text)



def get_cert_number(url):
	im = urllib.request.urlopen(url)
	text = re.findall(r'[0-9]{8}',image_to_string(Image.open(im)))
	return text



def get_image(id=333274691098):
	connection = ebaysdk.shopping.Connection(version='799', appid='vincentc-pokemon-PRD-5f95f0a8e-eb74953b',config_file=os.environ.get('EBAY_YAML'))
	response = connection.execute('GetSingleItem', {
	                'ItemID': id
	            })

	result = response.dict()
	print(result['Item']['PictureURL'][0])

	return result['Item']['PictureURL'][0]



get_image()


def commence_search(card_list, setname, grade ):
    for card_name in card_list:
        try:
            api = Connection(appid='vincentc-pokemon-PRD-5f95f0a8e-eb74953b', config_file=None)
            response = api.execute('findItemsByKeywords', {'keywords': 'gold star psa 10'})


            assert(response.reply.ack == 'Success')
            assert(type(response.reply.timestamp) == datetime.datetime)
            assert(type(response.reply.searchResult.item) == list)
            item = response.reply.searchResult.item

            search_results = response.dict()
            
            item = response.reply.searchResult.item[0]
            assert(type(item.listingInfo.endTime) == datetime.datetime)
            assert(type(response.dict()) == dict)
            #print (len(k['searchResult']['item']))

            print (search_results['searchResult']['item'][0]['itemId'])
            print (search_results['searchResult']['item'][1]['itemId'])

        except ConnectionError as e:

            print(e)
            print(e.response.dict())

    pass

    

commence_search([1],"neo", 10)

def lookup_psa(cert_number):  
  try:
    url = psa_url + str(cert_number)
    request=urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(request)
    data = response.read() # The data u need
    soup = BeautifulSoup(data, 'html.parser')

    psa_card_dict = {}
    for name in soup.find_all("td", class_="cert-grid-title"):
        label = name.parent.find_all('td')[0]
        label = label.get_text()
        value = name.parent.find_all('td')[-1]
        value = value.get_text()
        psa_card_dict[str(label)] = value
    
    return psa_card_dict
  except:
    return "errror getting cert number"





print(lookup_psa(27543232))



try:
    api = Connection(appid='vincentc-pokemon-PRD-5f95f0a8e-eb74953b', config_file=None)
    response = api.execute('findItemsByKeywords', {'keywords': 'mew ex play promo'})


    assert(response.reply.ack == 'Success')
    assert(type(response.reply.timestamp) == datetime.datetime)
    assert(type(response.reply.searchResult.item) == list)
    item = response.reply.searchResult.item
    k = response.dict()
    
    item = response.reply.searchResult.item[0]
    assert(type(item.listingInfo.endTime) == datetime.datetime)
    assert(type(response.dict()) == dict)
    #print (len(k['searchResult']['item']))
    #print (k['searchResult']['item'][0])



except ConnectionError as e:

    print(e)
    print(e.response.dict())

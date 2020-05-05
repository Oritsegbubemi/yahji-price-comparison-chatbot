# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

url_2 = "https://www.jumia.com.ng/"

categories = ["laptops", ]
laptops_categories = ["2-in-1-laptops","ultrabooks", "netbooks", "laptop-note"]

url_ke="https://www.jumia.co.ke/smartphones/?page=2"
#downloading all smartphone from second jumia page

###############################################################################
###############################################################################
def connect(url):
	fetched_items=requests.get(url)
	if fetched_items.status_code!=200:
		
		raise "ErrorGettingPage"
	try:
		soup=BeautifulSoup(fetched_items.text,"lxml")
		item_list=soup.find_all(attrs={"class":"sku -gallery"})
       
		offer_list=soup.find_all(attrs={"class":"sku -gallery -has-offers"})
		if item_list!=None and offer_list!=None:
			all_items=item_list+offer_list
	except AttributeError:
		
		raise AttributeError
	return all_items

def get_details(url):
    lst = connect(url)
    result = []
    for i in range(len(lst)):
        price = lst[i].find(attrs={"class":"price "}).find(attrs={"dir":"ltr"}).find(text=True)
        link = lst[i].find(attrs={"class":"link"})["href"].strip()
        name = lst[i].find(attrs={"class":"name"}).find(text=True).strip()
        
        price = int("".join(price.split(",")))
        
        result.append([name, price, link])
    return result

url = "https://www.jumia.com.ng/smartphones/?page=2"
laptops = ["apple", "hp", "acer", "asus", "lenovo", "microsoft", "dell", "toshiba"]
specific_laptop = "laptops/apple"

items = ["laptops", "phones"]
url_laptop = "https://www.jumia.com.ng/{}".format(items[0])

#res = get_details(url_laptop)




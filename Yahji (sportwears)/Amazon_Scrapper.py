import requests
import urllib2
from bs4 import BeautifulSoup
###############################################################################
def amazon_scrapper(x):
    result = []
    url="https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords={}".format(x)
    http=requests.get(url)
    soup=BeautifulSoup(http.text,"lxml")
###############################################################################
    img_url=urllib2.urlopen("https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords={}".format(x)).read()
    img_soup=BeautifulSoup(img_url)
    images = []
    images = img_soup.findAll('img')
    for image in images:
        print(image.get('src'))
###############################################################################
    item_list=soup.find_all(class_="a-row a-spacing-top-small")
    if item_list!=None: 
        all_items=item_list
    def get_details():  
        lst=all_items
        for i in range(len(all_items)):
            #price = lst[i].find(attrs={"class":"woocommerce-Price-amount amount"}).find(text=True)
            #link = lst[i].find(attrs={"class":"link"})["href"].strip()
            #price = int("".join(price.split(",")))
            name = lst[i].find(attrs={"class":"a-size-small a-color-base s-inline s-access-title a-text-normal"})
            result.append(["Name",name])
    get_details()
    return result[0:1]
print(amazon_scrapper("jersey"))


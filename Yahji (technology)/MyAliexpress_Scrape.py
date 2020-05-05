import requests
from bs4 import BeautifulSoup
###############################################################################
def url_request(x):
    result = []
    url="https://m.aliexpress.com/wholesale/{}.html?channel=direct&keywords={}".format(x)
    http=requests.get(url)
    soup=BeautifulSoup(http.text,"lxml")
    item_list=soup.find_all(class_="sku -gallery")
    offer_list=soup.find_all(class_="sku -gallery -has-offers")
    if item_list!=None and offer_list!=None: 
        all_items=item_list+offer_list
    def get_details():  
        lst=all_items
        for i in range(len(all_items)):
            price = lst[i].find(attrs={"class":"price "}).find(attrs={"dir":"ltr"}).find(text=True)
            link = lst[i].find(attrs={"class":"link"})["href"].strip()
            name = lst[i].find(attrs={"class":"name"}).find(text=True).strip()
            price = int("".join(price.split(",")))
            result.append([name,price,link])
    get_details()
    return result[0]



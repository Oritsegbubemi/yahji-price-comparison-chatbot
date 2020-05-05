"""
Beware of Promo price 
"""
import requests
from bs4 import BeautifulSoup
import pprint
###############################################################################
def zenith_scrapper(x):
    result, resultPrice = [], []
    #url="https://www.zenithsports.com.ng/product-category/{}".format(x)
    if x=="jeresy":
        url="https://www.zenithsports.com.ng/product-category/jersey"
    else:
       url="https://www.zenithsports.com.ng/product-category/jersey/{}".format(x)
    http=requests.get(url)
    soup=BeautifulSoup(http.text,"lxml")
    item_list=soup.find_all(class_="product_item")
    if item_list!=None: 
        all_items=item_list
    def get_details():  
        lst=all_items
        for i in range(len(all_items)):
            #price = lst[i].find(attrs={"class":"woocommerce-Price-amount amount"}).text
            price1 = lst[i].find_all("del","span")
            price2 = lst[i].find_all("ins")
            linkl = lst[i].find(attrs={"class":"woocommerce-LoopProduct-link woocommerce-loop-product__link"})["href"].strip()
            name = lst[i].find(attrs={"class":"product-title"}).find(text=True).strip()
            result.append(["Name",name,"Old Price",price1,"New Price",price2,"Link", linkl])
            #intprice=price[1:]
            #intprice=float("".join(intprice.split(",")))
            #resultPrice.append(intprice)
    get_details()
    return result[0:1]#, resultPrice[0]
print(zenith_scrapper("jersey"))
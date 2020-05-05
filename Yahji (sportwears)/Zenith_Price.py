import requests
from bs4 import BeautifulSoup
###############################################################################
def zenith_scrapper(x):
    result = []
    url="https://www.zenithsports.com.ng/product-category/{}".format(x)
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
            price = lst[i].find(attrs={"class":"woocommerce-Price-amount amount"}).text
            linkl = lst[i].find(attrs={"class":"woocommerce-LoopProduct-link woocommerce-loop-product__link"})["href"].strip()
            name = lst[i].find(attrs={"class":"product-title"}).find(text=True).strip()
            intprice=price[1:]
            intprice=float("".join(intprice.split(",")))
            result.append(["Name",name,"Price",price,"Link", linkl, "Real Price", intprice])
    get_details()
    return result[0:1]
print(zenith_scrapper("club-jersey"))
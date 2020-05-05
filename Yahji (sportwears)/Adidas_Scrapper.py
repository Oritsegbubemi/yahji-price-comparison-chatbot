import requests
from bs4 import BeautifulSoup
###############################################################################
def adidas_scrapper(x):
    result = []
    url="https://www.adidas.com.ng/us/{}".format(x)
    http=requests.get(url)
    soup=BeautifulSoup(http.text,"lxml")
    item_list=soup.find_all(class_="col-s-6 col-m-4 col-1-8 col-x1-6 no-gutters pip-column___3gy6t")
    if item_list!=None: 
        all_items=item_list  
    def get_details():  
        lst=all_items
        for i in range(len(all_items)):
            price = lst[i].find(attrs={"class":"gl-price"}).find(text=True)
            #link = lst[i].find(attrs={"class":"link"})["href"].strip()
            name = lst[i].find(attrs={"class":"gl-product-card__name gl-label gl-label--medium"}).find(text=True).strip()
            #brand = lst[i].find(attrs={"class":"brand"}).find(text=True).strip()
            #price = int("".join(price.split(",")))
            result.append(["Name",name,"Price",price])
            #result.append(["Name",name,"Brand",brand,"Price",price,"Link",link])
    get_details()
    return result[1:2]
print(adidas_scrapper("jerseys"))


import requests
from bs4 import BeautifulSoup
###############################################################################
def konga_scrapper(x):
    result = []
    
    url="https://www.konga.com/catalogsearch/result/?q={}".format(x)
    
    http=requests.get(url)
    print("Hello")
    soup=BeautifulSoup(http.text,"lxml")
    item_list=soup.find_all(class_="product-block-container")
    if item_list!=None: 
        all_items=item_list
    def get_details():  
        lst=all_items
        for i in range(len(all_items)):
            price = lst[i].find(attrs={"class":"special-price"}).find(text=True)
            link = lst[i].find(attrs={"class":"product-block-link"})["href"].strip()
            name = lst[i].find(attrs={"class":"product-name truncate"}).find(text=True).strip()
            #brand = lst[i].find(attrs={"class":"brand"}).find(text=True).strip()
            #price = int("".join(price.split(",")))
            result.append(["Name",name,"Price",price,"Link",link])
    get_details()
    return result[1:2]
print(konga_scrapper("jersey"))


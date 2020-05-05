import requests
from bs4 import BeautifulSoup
###############################################################################
def jiji_scrapper(x):
    result = []
    url="https://www.jiji.ng/search?query={}".format(x)
    http=requests.get(url)
    soup=BeautifulSoup(http.text,"lxml")
    item_list=soup.find_all(class_="sku -gallery -validate-size")
    offer_list=soup.find_all(class_="sku -gallery")
    offer_list2=soup.find_all(class_="mabaya sku -gallery")
    if item_list!=None and offer_list!=None and offer_list2!=None: 
        all_items=item_list+offer_list+offer_list2
    def get_details():  
        lst=all_items
        for i in range(len(all_items)):
            price = lst[i].find(attrs={"class":"price "}).find(attrs={"dir":"ltr"}).find(text=True)
            link = lst[i].find(attrs={"class":"link"})["href"].strip()
            name = lst[i].find(attrs={"class":"name"}).find(text=True).strip()
            brand = lst[i].find(attrs={"class":"brand"}).find(text=True).strip()
            price = int("".join(price.split(",")))
            result.append(["Name",name,"Brand",brand,"Price",price,"Link",link])
    get_details()
    return result[1:2]
print(jiji_scrapper("jersey"))



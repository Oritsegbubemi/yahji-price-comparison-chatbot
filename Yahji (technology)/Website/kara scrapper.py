import requests
from bs4 import BeautifulSoup
def url_request(x):
    result = []
    url="http://www.kara.com.ng/{}".format(x)
    http=requests.get(url)
    soup=BeautifulSoup(http.text,"lxml")
    item_first=soup.find_all(class_="item first")
    item_middle=soup.find_all(class_="item")
    item_last=soup.find_all(class_="item last")
    if item_first!=None and item_middle!=None and item_last!=None: 
        all_items=item_first#+item_middle+item_last
    def get_details():  
        lst=all_items
        for i in range(len(all_items)):
            price = lst[i].find(attrs={"class":"price"}).find(text=True)
            #link = lst[i].find(attrs={"class":"product-name"})["href"].strip()
            name = lst[i].find(attrs={"class":"product-name"}).find(text=True).strip()
            result.append([name,price])
    get_details()
    return result[0]
    
print(url_request("laptops"))

#######http://www.kara.com.ng/hp-laptops
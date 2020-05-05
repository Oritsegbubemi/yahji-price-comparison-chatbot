# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

main_url = "https://www.konga.com/"

laptops = ["acer", "apple", "asus", "dell", "hp", "lenovo", "microsoft", "toshiba"]
laptop_url = "https://www.konga.com/catalogsearch/result/?q=laptop&aggregated_brand=Acer&category_id=5230"

#def konga_laptop():
# with open("laptop.html", "r", encoding="utf-8") as f:
    # soup = BeautifulSoup(f, "lxml")

"https://www.konga.com/catalogsearch/result/?q=laptop&aggregated_brand=Acer&category_id=5230&sort=price%3Aasc"

def konga_laptop(arg):
    global soup, url_low, url_high
    if arg == "general":
        url = "https://www.konga.com/catalogsearch/result/?q=laptop&category_id=5230"
        url_low = url + "&sort=price%3Aasc"
        url_high = url + "&sort=price%3Adesc"
        
    else:
        url = "https://www.konga.com/catalogsearch/result/?q=laptop&aggregated_brand={}&category_id=5230".format(arg)
        url_low = url + "&sort=price%3Aasc"
        url_high = url + "&sort=price%3Adesc"
    
    pair = []
    for i in (url_low, url_high):
        http = requests.get(i)
        soup = BeautifulSoup(http.text, "lxml")
        
        p_name = soup.find("div", class_="product-name truncate")
        
        link = "https://www.konga.com" + p_name.find("a").get("href")
        name = p_name.text.replace("\n","")
        
        price = soup.find("div", class_="original-price original-price-bold").text
        pair.append([name,price,link])

    
    return pair

"https://www.konga.com/mobile-phones"

h = "https://www.konga.com/catalogsearch/result/?category_id=7539&aggregated_brand={}".format("Apple")

phones = ["apple", "afrione", "alcatel", "blackberry", "gionee", "htc", "huawei", "infinix",
          "innjoo", "itel", "lenovo", "lg", "motorola", "nokia", "samsung", "sony", "techno",
          "xiaomi", "zte"]

def konga_phone(arg):
    if arg != "general":
        url = "https://www.konga.com/catalogsearch/result/?category_id=7539&aggregated_brand={}".format(arg)
        url_low = url + "&sort=price%3Aasc"
        url_high = url + "&sort=price%3Adesc"
    else:
        url_low = "https://www.konga.com/catalogsearch/result/?category_id=7545&sort=price%3Aasc"
        url_high = "https://www.konga.com/catalogsearch/result/?category_id=5297&sort=price%3Adesc"
    
    pair = []
    for i in (url_low, url_high):
        http = requests.get(i)
        soup = BeautifulSoup(http.text, "lxml")
        
        p_name = soup.find("div", class_="product-name truncate")
        
        link = "https://www.konga.com" + p_name.find("a").get("href")
        name = p_name.text.replace("\n","")
        
        price = soup.find("div", class_="original-price original-price-bold").text
        pair.append([name,price,link])

    
    return pair

def search_konga(msg):
    global category, product, result
    message = msg.lower()
    p_present = [i for i in phones+["iphone", "iphones" "i-phone", "i phone"] if i in message]
    l_present = [i for i in laptops if i in message]
    if len(p_present) != 0:
        product = p_present[0]
        category = "phone"
    elif len(l_present) != 0:
        product = l_present[0]
        category = "laptop"
    else:
        product = "general"
        l_word = "laptop" in message
        p_word = "phone" in message
        if l_word:
            category = "laptop"
        elif p_word:
            category = "phone"
        
    if category == "phone":
        result = konga_phone(product)
        
#    elif category == "laptop" and product == "general":
#        result = konga_phone(product)
        
    elif category == "laptop":
        result = konga_laptop(product)
    
    txt0 = "Cheapest price on Konga:\n"
    txt1 = "Product Name: " + result[0][0] + "\nPrice: " + result[0][1] + "\nLink: " + result[0][2]
    
    txt2 = "Most Expensive price on Konga:\n"
    txt3 = "Product Name: " + result[1][0] + "\nPrice: " + result[1][1] + "\nLink: " + result[1][2]
    return txt0 + txt1 +"*#split#*"+ txt2 + txt3

#f = konga_phone("sony")
#g = konga_phone("general")

#res = search_konga("i need to get a good laptop")

#    section = soup.find("section", class_="products -mabaya")
#    a_tags = section.find_all("a", class_="link")
#    link = a_tags[0].get("href")
#    name = a_tags[0].find("h2", class_="title").text.replace("\xa0", "")
#    price = int(a_tags[0].find("span", class_="price").text.split()[-1].replace(",", ""))

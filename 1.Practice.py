###############################################################################1
#IMPORT ALL NEEDED LIBRARIES AND MODULES
import nltk, re, random, sqlite3, requests
from bs4 import BeautifulSoup
from sklearn.svm import SVC
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from MyJumia_Scrape import jumia_request
from MyKara_Scrape import kara_request
from MyDealday_Scrape import dealday_request
#from MyAliexpress_Scrape import url_request
#from konga_scraper import konga_laptop, konga_phone

###############################################################################2
#NLTK FOR GOOD PATTERNING
nltk.data.path.append('./nltk_data/')
stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for i in tokens:
        stemmed.append(stemmer.stem(i))
    return stemmed
def tokenize(text):
    tokens = nltk.word_tokenize(text)
    #Stems each token
    stems = stem_tokens(tokens, stemmer)
    return stems

#REMOVE STOP WORDS FROM THE USER INPUTS
stopwords_list = ["i", "my", "me", "is", "a", "an"]
vectorizer = TfidfVectorizer(tokenizer=tokenize, analyzer='word', lowercase=True, stop_words=stopwords_list)
def remove_punctuation(message):
    tokens = word_tokenize(message)
    #Removing Punctuations here:
    tokens_clean = [re.sub(r'[^a-zA-Z0-9{}]' ,'',each_word) for each_word in tokens] 
    tokens_final = [each_word.lower() for each_word in tokens_clean if len(each_word)]
    return tokens_final

###############################################################################3
#OPENING ALL FILES THAT ARE NEEDED
with open('dataset/opening.txt', 'r', encoding='utf-8') as f:
    opening = [(i.replace('\n', ''), 'opening') for i in f.readlines()]   
with open('dataset/opening2.txt', 'r', encoding='utf-8') as f:
    opening2 = [(i.replace('\n', ''), 'opening2') for i in f.readlines()]    
with open('dataset/greetings/greetings1.txt', 'r', encoding='utf-8') as f:
    greetings1 = [(i.replace('\n', ''), 'greetings1') for i in f.readlines()]    
with open('dataset/greetings/greetings2.txt', 'r', encoding='utf-8') as f:
    greetings2 = [(i.replace('\n', ''), 'greetings2') for i in f.readlines()]    
with open('dataset/greetings/greetings1_resp.txt', 'r', encoding='utf-8') as f:
   greetings1_resp = [(i.replace('\n', ''), 'greetings1_resp') for i in f.readlines()]
with open('dataset/greetings/greetings2_resp.txt', 'r', encoding='utf-8') as f:
    greetings2_resp = [(i.replace('\n', ''), 'greetings2_resp') for i in f.readlines()]    
with open('dataset/feelings/happy.txt', 'r', encoding='utf-8') as f:
    happy = [(i.replace('\n', ''), 'happy') for i in f.readlines()]
with open('dataset/feelings/sad.txt', 'r', encoding='utf-8') as f:
    sad = [(i.replace('\n', ''), 'sad') for i in f.readlines()]   
with open('dataset/other.txt', 'r', encoding='utf-8') as f:
    other = [(i.replace('\n', ''), 'other') for i in f.readlines()]
with open('dataset/other_reply.txt', 'r', encoding='utf-8') as f:
    other_reply = [(i.replace('\n', ''), 'other_reply') for i in f.readlines()]
with open('dataset/user_input.txt', 'r', encoding='utf-8') as f:
    user_input = [(i.replace('\n', ''), 'user_input') for i in f.readlines()]  
with open('dataset/product_inquiry.txt', 'r', encoding='utf-8') as f:
    product_inquiry = [(i.replace('\n', ''), 'product_inquiry') for i in f.readlines()]  
with open('dataset/FAQ.txt', 'r', encoding='utf-8') as f:
    FAQ = [(i.replace('\n', ''), 'FAQ') for i in f.readlines()]
with open('dataset/end.txt', 'r', encoding='utf-8') as f:
    end = [(i.replace('\n', ''), 'end') for i in f.readlines()]

###############################################################################4
#ASSIGNING THE ITEMS OF THE FILE TO A LIST    
texts, labels = [],[]
for i in opening:
    texts.append(i[0])
    labels.append(i[1])    
for i in opening2:
    texts.append(i[0])
    labels.append(i[1]) 
for i in greetings1:
    texts.append(i[0])
    labels.append(i[1])
for i in greetings2:
    texts.append(i[0])
    labels.append(i[1])
for i in greetings1_resp:
    texts.append(i[0])
    labels.append(i[1])  
for i in greetings2_resp:
    texts.append(i[0])
    labels.append(i[1])
for i in happy:
    texts.append(i[0])
    labels.append(i[1])
for i in sad:
    texts.append(i[0])
    labels.append(i[1])  
for i in product_inquiry:
    texts.append(i[0])
    labels.append(i[1])
for i in end:
    texts.append(i[0])
    labels.append(i[1])
for i in other:
    texts.append(i[0])
    labels.append(i[1])  
for i in other_reply:
    texts.append(i[0])
    labels.append(i[1])
for i in user_input:
    texts.append(i[0])
    labels.append(i[1])
for i in FAQ:
    texts.append(i[0])
    labels.append(i[1])
    
###############################################################################5
#CLASSIFICATION OF THE FILES AND USER INPUTS
X_vector = vectorizer.fit_transform(texts)
clf = SVC(kernel='linear',probability=True)
clf.fit(X_vector,labels)
def classifier(message):
    out_put = []
    message_tokens = remove_punctuation(message)
    message_string = (' '.join(message_tokens))
    out_put.append(message_string)
    out_put_vector = vectorizer.transform(out_put)
    #print(clf.predict_proba(out_put_vector))
    out_put_class = clf.predict(out_put_vector)
    return out_put_class[0]

###############################################################################6
#OPENING TAG
display=""
welcome=["Hello","Start Conversation: ","Hi my name is Nicole. What's your name? ","Enter a reply: "]
print('\033[1m'+welcome[0]+ '\033[0m')
first_input=input(welcome[1])
username=input(welcome[2])
new_user=username.lower()
if "i\'m " in new_user:
    username=new_user[4:]
elif "my name is " in new_user:
    username=new_user[11:]
elif "i am " in new_user:
    username=new_user[5:]
    
def opening_tag():    
    i=random.choice(opening)  
    display=i[0] + username.capitalize()
    print(display) 
    j=random.choice(greetings2)
    display2=username.capitalize()+ " " +j[0]
    print(display2)
    input(welcome[3])
    k=random.choice(greetings2_resp)  
    display3=username.capitalize()+ " " + k[0]
    print(display3)
opening_tag()

###############################################################################12
#PRODUCT INQUIRY
available_products = ["laptops", "phones"]
alt_spellings = ["laptop", "phone"]
spellings_dict = {"laptop":available_products[0], "phone":available_products[1]}
laptops = ["apple", "hp", "acer", "asus", "lenovo", "microsoft", "dell", "toshiba","fujitsu"]
#To return cheapest and most expensive item in search_product link.
def price_pair(lst):
    prices = [i[1] for i in lst]
    min_price, max_price = min(prices), max(prices)
    pairs_index = prices.index(min_price), prices.index(max_price)
    return pairs_index

def compare_product(x):
    global pair_result
    lst=jumia_request(x)
    if len(lst) != 0:
        pairs = price_pair(lst)
        pair_result = []
        for i in pairs:
            product, price, link = lst[i][0], lst[i][1], lst[i][2]
            res = [product, price, link]
            pair_result.append(res)
        pr = pair_result
        txt1 = "Cheapest Price on Jumia:\nName: {}\nPrice: {} Naira\nLink: {}".format(pr[0][0], pr[0][1], pr[0][2])#(name, price, link)
        txt2 = "Most Expensive Price on Jumia:\nName: {}\nPrice: {} Naira\nLink: {}".format(pr[1][0], pr[1][1], pr[1][2])
        text = txt1 +"\n\n"+ txt2    
    else:
        text = "Wasn't able to get that at the moment...\nMaybe not currently available." 
    return text
"""
phone = compare_product("smartphones/?page=2")
laptop = compare_product("laptops")
print("PHONE!!!!!!!!!!!\n"+phone)
print("LAPTOP!!!!!!!!!!\n"+laptop)
"""

def jumia_laptop(a):
    if a in laptops:
        x="laptops/{0}".format(a)
        lst=jumia_request(x)
        if len(lst) != 0:
            for i in lst:
                for j in i:
                    print(j)
            text=''
        else:
            text = "Wasn't able to get that at the moment...\nMaybe not currently available." 
        return text
    else:
        return "Sorry, We don't have such laptop in our database\nPlease check your spelling"

def kara_laptop(a):
    if a in laptops:
        x="laptops/{0}".format(a)
        lst=kara_request(x)
        if len(lst) != 0:
            for i in lst:
                for j in i:
                    print(j)
            text=''
        else:
            text = "Wasn't able to get that at the moment...\nMaybe not currently available." 
        return text
    else:
        return "Sorry, We don't have such laptop in our database\nPlease check your spelling"

def dealday_laptop(a):
    if a in laptops:
        x="laptops/{0}".format(a)
        lst=dealday_request(x)
        if len(lst) != 0:
            for i in lst:
                for j in i:
                    print(j)
            text=''
        else:
            text = "Wasn't able to get that at the moment...\nMaybe not currently available." 
        return text
    else:
        return "Sorry, We don't have such laptop in our database\nPlease check your spelling"
"""
######Search Laptop based on type
laptop=search_laptop(laptop_type)
print("Laptop!!!!!!!!!\n"+laptop)
"""
###############################################################################7
#SPECIFY TYPE OF LAPTOP
def available():
    text="The Laptops available for now are\nHP\nApple\nDell\nAcer\nAsus\nLenovo\nMicrosoft\nToshiba\nfujitsu"
    return text
def specify():
    details=["You have to specify","Type: ","Price range(In Figure, Excluding Commas): " ]
    print(details[0])
    print(available())
    laptop_type=input(details[1])
    try: 
        laptop_price=int(input(details[2]))
    except:
        text="Price must be an integer"
        return text 
    con = sqlite3.connect('laptop.db')
    co = con.cursor()
    def create_table():
        co.execute('CREATE TABLE IF NOT EXISTS '+username+'(type TEXT, price TEXT)')
    def data_entry(a,b):
        co.execute("INSERT INTO "+username+" VALUES (?,?)",(a,b))
        con.commit()
        co.close()
        con.close()
    create_table()
    data_entry(laptop_type,laptop_price)
    print( "Okay... Request loading...")
    """
    ######Comapre Product
    laptop = compare_product("laptops")
    print("LAPTOP!!!!!!!!!!\n"+laptop)
    """
    
    ######Search Laptop based on type
    j_laptop=jumia_laptop(laptop_type)
    k_laptop=kara_laptop(laptop_type)
    d_laptop=dealday_laptop(laptop_type)
    print("Laptop!!!!!!!!!\n"+j_laptop, k_laptop, d_laptop)
    
    
def questions(se):
    reply= open('dataset/FAQ.txt') 
    for line in reply:
        if line.startswith(se) != -1: 
            real=line.split("-")
            return real[1]
def user(sent):
    data=open('dataset/user_input.txt')
    for line in data:
        if line.startswith(sent)!=-1:
            real=line.split("-")
            return real[1]
    
###############################################################################8
def response(classification):
    if classification == "greetings1": 
        i=random.choice(greetings1_resp)  
        return i[0]
    elif classification == "greetings2":
        j=random.choice(greetings2_resp)  
        return j[0]
    elif classification == "product_inquiry":
       return specify()    
    elif classification == "happy":
        return "Good to hear"
    elif classification == "sad":
        return "I'm sorry. I will ask my programmer to improve on me"
    elif classification == "other":
        k=random.choice(other_reply)  
        return k[0]
    elif classification == "end":
        return "Cool... Thanks. Have a nice day"
    elif classification =="user_input":
        return "user input"
    elif classification=="FAQ":
        return "Thinking..."

###############################################################################9
##WIKIPEDIA ADDED FEATURES
def connect(x):
    url="https://em.n.wikipedia.org/wiki/{0}".format(x)
    fetched_items=requests.get(url)
    if fetched_items.status_code!=200:
        return "Error"
    try:
        soup=BeautifulSoup(fetched_items.text,"lxml")
        items=soup.find_all("p")
        sentence_tokens=nltk.sent_tokenize(items)
        for i in sentence_tokens:
            print(i+"\n")
    except AttributeError:
        raise AttributeError

def connec(h):
    return "youuuu"

        
###############################################################################10
#LOOP THE CHATBOT
sent_result=dict()
yes=True
sent_other,sent_happy,sent_sad=[],[],[]
while yes:
    sentence=input("Enter the text: ")
    open_tag=random.choice(opening)
    result = classifier(sentence)
    #Create a list for the other file
    if result=="other":
        sent_other.append(sentence)
        sent_result[result]=sent_other
    elif result=="happy":
        sent_happy.append(sentence)
        sent_result[result]=sent_happy
    elif result=="sad":
        sent_sad.append(sentence)
        sent_result[result]=sent_sad
    else: 
        sent_result[result]=sentence
    #create a path for the frequently asked questions
    resp=response(result)
    print(resp)
    if resp=="Thinking...":
        print(questions(sentence))
    if resp=="user input":
        print(user(sentence))
    if resp=="Cool... Thanks. Have a nice day":
        yes=False

###############################################################################11
#OPEN USER DATABASE
for k in sent_result:
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    def create_table():
        c.execute('CREATE TABLE IF NOT EXISTS '+username+'(id_num TEXT, message TEXT)')
    def data_entry(ran,j):
        if k=="other":
            for j in sent_result[k]:  
                c.execute("INSERT INTO "+username+" VALUES (?,?)",(ran,j))
                def read_data(arg):
                    c.execute("SELECT * FROM "+username+" WHERE id_num='{}'".format(arg))
                    with open('dataset/user_input.txt', 'a', encoding='utf-8') as f:
                        f.write(j+ "-")
                #connect(j)
                read_data(j)
                with open('dataset/user_input.txt', 'a', encoding='utf-8') as f:
                        f.write(connec(j)+"\n")
        elif k=="sad":
            for j in sent_result[k]:  
                c.execute("INSERT INTO "+username+" VALUES (?,?)",(ran,j))
        elif k=="happy":
            for j in sent_result[k]:  
                c.execute("INSERT INTO "+username+" VALUES (?,?)",(ran,j))
        else:
            c.execute("INSERT INTO "+username+" VALUES (?,?)",(ran,sent_result[ran]))
        conn.commit()
        c.close()
        conn.close()
    create_table()
    data_entry(k,sent_result[k])
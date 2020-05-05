###############################################################################1
#IMPORT ALL NEEDED LIBRARIES AND MODULES
import nltk, re, random, sqlite3, requests
from bs4 import BeautifulSoup
from sklearn.svm import SVC
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
#from Zenith_Scrapper import zenith_scrapper
#from Jumia_Scrapper import jumia_scrapper
#from Adidas_Scrapper import adidas_scrapper
#from Amazon_Scrapper import amazon_scrapper
#from Konga_Scrapper import konga_scrapper
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
    out_put_class = clf.predict(out_put_vector)
    return out_put_class[0]

###############################################################################6
##Opening Tags
""""
    ########Edit the input from the user
    def username():
        username=input("Enter name: ")
"""
welcome=["Hello","Start Conversation: ","Hi my name is Nicole. What's your name? ","Enter a reply: "]
print(welcome[0])
first_input=input(welcome[1])
username=input(welcome[2])
new_user=username.capitalize()
real_name=new_user.split(" ")
if(real_name[-1]==""):
    username=real_name[-2]
else:
    username=real_name[-1]
###############################################################################7
##Product_Inquiry
    
###############################################################################8
##Classification
def response(classification):
    if classification == "greetings1":
        i=random.choice(greetings1_resp)
        return i[0]
    elif classification == "greetings2":
        j=random.choice(greetings2_resp)
        return j[0]
    elif classification == "product_inquiry":
        return "Ohh, Yes I am product"
    elif classification == "happy":
        return "Good to hear"
    elif classification == "sad":
        return "I'm sorry. I will ask my programmer to improve on me"
    elif classification == "other":
        k=random.choice(other_reply)
        return k[0]
    elif classification =="user_input":
        return "user input"
    elif classification=="FAQ":
        return "Thinking..."
    elif classification == "end":
        return "Cool... Thanks. Have a nice day"
    
###############################################################################   
#FAQ
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
sent_other,sent_happy,sent_sad, sent_product=[],[],[],[]
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
    elif result=="product_inquiry":
        sent_product.append(sentence)
        sent_result[result]=sent_product
    else:
        sent_result[result]=sentence
    resp=response(result)
    print(resp)
    ###Re-edit
    if resp=="Thinking...":
        print(questions(sentence))
    if resp=="user input":
        print(user(sentence))
    if resp=="Cool... Thanks. Have a nice day":
        yes=False

###############################################################################11
#OPEN USER DATABASE
for k in sent_result:
    conn = sqlite3.connect('userDB.db')
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
        elif k=="product_inquiry":
            for j in sent_result[k]:  
                c.execute("INSERT INTO "+username+" VALUES (?,?)",(ran,j))
        else:
            c.execute("INSERT INTO "+username+" VALUES (?,?)",(ran,sent_result[ran]))
        conn.commit()
        c.close()
        conn.close()
    create_table()
    data_entry(k,sent_result[k])
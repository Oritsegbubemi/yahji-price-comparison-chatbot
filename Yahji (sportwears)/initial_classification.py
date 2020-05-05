import nltk, re
from sklearn.svm import SVC
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

from MyJumia_Scrape import get_details
#from konga_scraper import konga_laptop, konga_phone
#from nltk.corpus import stopwords
#from nltk.stem.wordnet import WordNetLemmatizer
#lmtzr = WordNetLemmatizer()
#lmtzr.lemmatize('cars')
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

stopwords_list = ["i", "my", "me", "is", "a", "an"]
vectorizer = TfidfVectorizer(tokenizer=tokenize, analyzer='word', lowercase=True, stop_words=stopwords_list)

def remove_punctuation(message):
    tokens = word_tokenize(message)
    #Removing Punctuations here:
    tokens_clean = [re.sub(r'[^a-zA-Z0-9]' ,'',each_word) for each_word in tokens]
    tokens_final = [each_word.lower() for each_word in tokens_clean if len(each_word)]
    return tokens_final

###############################################################################
with open('dataset/greetings.txt', 'r', encoding='utf-8') as f:
    greetings = [(i.replace('\n', ''), 'greetings') for i in f.readlines()]
    
with open('dataset/product_inquiry.txt', 'r', encoding='utf-8') as f:
    product_inquiry = [(i.replace('\n', ''), 'product_inquiry') for i in f.readlines()]

with open('dataset/end.txt', 'r', encoding='utf-8') as f:
    end = [(i.replace('\n', ''), 'end') for i in f.readlines()]
    
texts, labels = [],[]
for i in greetings:
    texts.append(i[0])
    labels.append(i[1])
    
for i in product_inquiry:
    texts.append(i[0])
    labels.append(i[1])

for i in end:
    texts.append(i[0])
    labels.append(i[1])

###############################################################################

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

available_products = ["laptops", "phones"]
alt_spellings = ["laptop", "phone"]
spellings_dict = {"laptop":available_products[0], "phone":available_products[1]}

"""
def response_old(msg):
    message = msg.lower()
    classification = classifier(message)
    if classification == "greetings":
        return "Greetings"
    elif classification == "end":
        return "Cool..."
    else:
        p = [i for i in available_products+alt_spellings if i in message]
        if len(p) == 0:
            return "Requests not completed either because product is not available or couldn't process message"
        #Deal with this:
        else:
            return "{} is available".format(p[0])
"""

def response(classification):
    if classification == "greetings":
        return "Greetings"
    elif classification == "end":
        return "Cool..."

laptops = ["apple", "hp", "acer", "asus", "lenovo", "microsoft", "dell", "toshiba"]

def check_product(msg):
    message = msg.lower()
    p = [i for i in available_products+alt_spellings if i in message]
    if len(p) == 0:
        return ["absent", ""]
    #Deal with this:
    else:
        if p[0] in spellings_dict:
            k = spellings_dict[p[0]]
        else:
            k = p[0]   
        q = [i for i in laptops if i in message]
        if q: k="laptops/{}".format(q[0])
        return ["present", k]
#       return "{} is available".format(p[0])

#print(check_product("i need an asus laptop"))

def search_product(product):
    global pair_result
    url = "https://www.jumia.com.ng/smartphones/?page=2/{}".format(product)
    lst = get_details(url)
    #lst2 = konga_laptop()  
    if len(lst) != 0:
        pairs = price_pair(lst)
        pair_result = []
        for i in pairs:
            product, price, link = lst[i][0], lst[i][1], lst[i][2]
            res = [product, price, link]
            pair_result.append(res)
        pr = pair_result
        txt1 = "Cheapest Price on Jumia:\nName: {}\n\nPrice: {} Naira\n\nLink: {}".format(pr[0][0], pr[0][1], pr[0][2])#product, price, link)
        txt2 = "Most Expensive Price on Jumia:\nName: {}\n\nPrice: {} Naira\n\nLink: {}".format(pr[1][0], pr[1][1], pr[1][2])
        #The split is just for convenience so this function returns a string, and split in the main code later.
        text = txt1 +"*#split#*"+ txt2    
    else:
        text = "Wasn't able to get that at the moment...\nMaybe not currently available." 
    return text

#To return cheapest and most expensive item in search_product link.
def price_pair(lst):
    prices = [i[1] for i in lst]
    min_price, max_price = min(prices), max(prices)
    pairs_index = prices.index(min_price), prices.index(max_price)
    return pairs_index#[min_price, max_price]

result = search_product("laptops")

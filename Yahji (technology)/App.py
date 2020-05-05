from flask import Flask, request
import json
import requests
from Chatbot import classifier, response, check_product, search_product
from konga_scraper import search_konga

###############################################################################
import sqlite3

conn = sqlite3.connect("Nicole.db")
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS items(chat_id TEXT, message TEXT)")

def data_entry(arg):
    c.execute("INSERT INTO items VALUES(?,?)",
              (arg[0], arg[1]))
    conn.commit()

def read_data(arg):
    c.execute("SELECT * FROM items WHERE chat_id='{}'".format(arg))
    data = c.fetchall()
    return data
###############################################################################

app = Flask(__name__)

PAT = 'EAAXsaMwwIBsBAK86bqZBsKV9VqsywJW70m9mB1mOHFlCvKmuNjBP326cYTL7ZAhUAjCcb5aq1zcetOVpekb5ZB6f4xhP6ewEOtgzyORUN02DevwHPFQq1ATxGbbiHUJmGncZBDCrIDY7ZAW5kAMuPWd9IvZA0cLxQe2L83h7FhggZDZD'

create_table()

@app.route('/', methods=['GET'])
def handle_verification():
  print("Handling Verification.")
  if request.args.get('hub.verify_token', '') == 'trollex_nicole_bot':
    print("Verification successful!")
    return(request.args.get('hub.challenge', ''))
  else:
    print("Verification failed!")
    return('Error, wrong validation token')

@app.route('/', methods=['POST'])
def handle_messages():
  print("Handling Messages")
  payload = request.get_data()
  print(payload)
  
  for sender, message in messaging_events(payload):
    print("Incoming from %s: %s" % (sender, message))
    
    arg = str(sender)
    d = read_data(arg)
    if len(d) == 0:
        d = "#@$#$%@$%@$"
    else:
        d = d[-1][-1]
    if d != message:
        send_message(PAT, sender, message)
        arg = [str(sender), message]
        data_entry(arg)
  return "ok"

def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"

                    

def send_message(token, recipient, text):
  """Send the message text to recipient with id recipient.
  """
  
  msg = text.lower()
  msg = str(msg)
  classification = classifier(msg)
  if classification != "product_inquiry":
      bot_msg = response(classification)
  else:
      product_status = check_product(msg)
      if product_status[0] == "absent":
          bot_msg = "No information about that."
      else:
          txt = search_product(product_status[1])
          txt_konga = 0
          try:
              txt_konga = search_konga(msg)
          except Exception as e:
              pass
          txt_konga = txt.replace("*#split#*", "")
          
          bot_msg = txt + "\n\n" + txt_konga
          
  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": bot_msg}#.decode('unicode_escape')}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print(r.text)

if __name__ == '__main__':
  app.run()
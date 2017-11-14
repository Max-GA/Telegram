import json
import bs4 as bs
import urllib.request
import requests

TOKEN = "433782927:AAGhtZEFd6mx59OAHMiGROlV7R4_xgxILZI/"

HTTP_URL = "https://api.telegram.org/bot"+TOKEN

#SAUCE = urllib.request.urlopen(HTTP_STR+"/getUpdates").read()
#soup = bs.BeautifulSoup(SAUCE, "lxml")
#JSON = json.loads(SAUCE.decode("utf-8"))
#print()
#print(SAUCE.decode("utf-8"))
#print()
#print(JSON["result"][0]["message"]["from"]["id"])

def get_updates_json(url):
    args = {"timeout": 100, "offset": None}
    result = requests.get(url+"getUpdates", data=args)
    return result.json()

def last_update(data):
    result = data["result"]
    total_updates = len(result)-1
    return result[total_updates]

def get_chat_id(update):
    chat_ID = update["message"]["chat"]["id"]
    return chat_ID

def send_mess(chat, text):
    args = {"chat_id": chat, "text": text}
    result = requests.post(HTTP_URL+"sendMessage", data=args)
    return result

CHAT_ID = get_chat_id(last_update(get_updates_json(HTTP_URL)))
send_mess(CHAT_ID, "Hi")
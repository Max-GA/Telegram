import json
import bs4 as bs
import urllib.request
import requests
import time
import threading
import Profiles


class Bot(object):
    def __init__(self):
        self.Contacts = Profiles.Contacts()
        self.URL = "https://api.telegram.org/bot433782927:AAGhtZEFd6mx59OAHMiGROlV7R4_xgxILZI/"
        self.Conversations = self.Contacts.getIDs()
        self.Handling_IDs = []
        self.Last_Result = None
        self.Update_ID = int
        self.Chat_ID = int

    def start(self):
        self.Last_Result = self.lastUpdate(self.getUpdates_Json())
        self.Update_ID = self.getUpdateID(self.Last_Result)
        while True:
            self.Last_Result = self.lastUpdate(self.getUpdates_Json())
            new_Update_ID = self.getUpdateID(self.Last_Result)
            self.Chat_ID = self.getID(self.Last_Result)
            if new_Update_ID != self.Update_ID and (self.Chat_ID not in self.Handling_IDs):
                self.Handling_IDs.append(self.Chat_ID)
                manager = threading.Thread(target=self.handler, args=(self.Last_Result,))
                manager.start()
                self.Update_ID = new_Update_ID

    def handler(self, Result):
        Chat_ID = self.getID(Result)
        Update_ID = self.getUpdateID(Result)

        if Chat_ID in self.Conversations:
            if self.getText(Result) == "/help":
                self.help(Chat_ID)
            elif self.getText(Result) == "/commands":
                self.commands(Chat_ID)
            elif self.getText(Result) == "/time":
                self.time(Chat_ID)
            else:
                self.sendMessage(Chat_ID, "Sorry! I couldn't understand you :(")
        else:
            self.sendMessage(Chat_ID, "Hey !\nI don't know you !\nCan you please tell me your name ?")
            registered = False
            while not registered:
                new_Result = self.lastUpdate(self.getUpdates_Json())
                new_Update_ID = self.getUpdateID(new_Result)
                if new_Update_ID != Update_ID and self.getID(new_Result) == Chat_ID:
                    Name = self.getText(new_Result)
                    self.sendMessage(Chat_ID, "Nice to meet you , {}!\nYou can see what I can do by typing /help or /commands\nThank you for talking with me :)".format(Name))
                    self.Update_ID = new_Update_ID

                    self.Contacts.newContact(Name, Chat_ID)
                    self.Conversations = self.Contacts.getIDs()
                    registered = True
        self.Handling_IDs.pop(self.Handling_IDs.index(Chat_ID))

    def help(self, Chat_ID):
        Name = self.Contacts.getName(Chat_ID)
        text = """Hello {} :)\nDon't worry , I'm actually not that complicated :)\nMy name is PyCHT_Bot , named after the language in which I was programmed\nMy creator is a hobby-Coder who brought me to life , if you want to contact him send him a message to Maximilian.Gaurov@web.de\n\nBut enough about my father , let's talk about me :)\n/help ... well ... you typed it so you knew this command already\n/commands will show you everything that I can do\nType /time and I will send you the time , I know not very impressive but it's free so why not\n\nAnd that's it... Not very much but you can try to talk with me normally, maybe I'll respond ;) """.format(Name)
        self.sendMessage(Chat_ID, text)

    def commands(self, Chat_ID):
        text="""/commands - list all commands\n/help - an explanation of what I am\n/time - sends you the time
        """
        self.sendMessage(Chat_ID, text)


    def time(self, Chat_ID):
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        if 12 > int(time_now.split(" ")[1].split(":")[0]) >= 0:
            self.sendMessage(Chat_ID, "Good morning , it is the " + time_now.split(" ")[0] + " and the time is : " + time_now.split(" ")[1])
        elif 18 > int(time_now.split(" ")[1].split(":")[0]) >= 12:
            self.sendMessage(Chat_ID, "Good evening , it is the " + time_now.split(" ")[0] + " and the time is : " + time_now.split(" ")[1])
        elif 24 > int(time_now.split(" ")[1].split(":")[0]) >= 18:
            self.sendMessage(Chat_ID, "Good night , it is the " + time_now.split(" ")[0] + " and the time is : " + time_now.split(" ")[1])


    def getUpdates_Json(self):
        args = {"timeout": 100, "offset": None}
        DATA = requests.get(self.URL+"getUpdates", data = args)
        return DATA.json()

    def lastUpdate(self, data):
        JSON_Results = data["result"]
        return JSON_Results[-1]

    def getID(self, update):
        ID = update["message"]["chat"]["id"]
        return ID

    def getName(self, update):
        Name = update["message"]["chat"]["first_name"]
        return Name

    def getUpdateID(self, data):
        UpdateID = data["update_id"]
        return UpdateID

    def getText(self, update):
        Text = update["message"]["text"]
        return Text

    def sendMessage(self, ID, text):
        args = {"chat_id" : ID, "text": text}
        result = requests.post(self.URL+"sendMessage", data=args)
        return result


if __name__ == "__main__":
    ActivateBot = Bot()
    ActivateBot.start()

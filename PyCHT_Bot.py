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
        self.Conversations = self.loadConversations()
        self.Handling_IDs = []
        self.Last_Result = None
        self.Update_ID = int
        self.Chat_ID = int

    def start(self):
        self.Last_Result = self.lastUpdate(self.getUpdates_Json())
        self.Update_ID = self.getUpdateID(self.Last_Result)
        while True:
<<<<<<< HEAD
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
=======
            LAST = self.lastUpdate(self.getUpdates_Json())
            UPDATE_ID_NEW = self.getUpdateID(LAST)
            if UPDATE_ID_NEW != UPDATE_ID_OLD:
                ID = self.getID(LAST)
                if ID not in self.NewContacts:
                    if ID in self.Conversations:
                        text = self.getText(ID, LAST)
                        self.respondText(text, ID)
                    else:
                        self.NewContacts.append(ID)
                        hallo_thread = threading.Thread(target=self.sayHello, args=(ID,UPDATE_ID_NEW))
                        hallo_thread.start()
                UPDATE_ID_OLD = UPDATE_ID_NEW

    def respondText(self, Text, ID):
        if Text == "/uhrzeit":
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            if int(time_now.split(" ")[1].split(":")[0]) >= 0 and int(time_now.split(" ")[1].split(":")[0]) < 12:
                self.sendMessage(ID, "Guten Morgen , es ist der " + time_now.split(" ")[0] + " und die Zeit beträgt : " + time_now.split(" ")[1])
            elif int(time_now.split(" ")[1].split(":")[0]) >= 12 and int(time_now.split(" ")[1].split(":")[0]) < 18:
                self.sendMessage(ID, "Guten Mittag , es ist der " + time_now.split(" ")[0] + " und die Zeit beträgt : " + time_now.split(" ")[1])
            elif int(time_now.split(" ")[1].split(":")[0]) >= 18 and int(time_now.split(" ")[1].split(":")[0]) < 24:
                self.sendMessage(ID, "Guten Abend , es ist der " + time_now.split(" ")[0] + " und die Zeit beträgt : " + time_now.split(" ")[1])
        elif Text == "/help":
            self.sendMessage(ID, "Keine Sorge ich bin nicht so kompliziert ;)\n\n"
                                 "Ich bin ein kleiner hobby-programmierter Bot welcher dir viele unnütze Sache sagen kann!\n"
                                 "Ich weiß ... nicht sehr spektakulär aber ich entwickle mich immer weiter und werde somit auch immer interessanter !\n\n"
                                 "Meine Commands : \n"
                                 "/uhrzeit Gibt dir die jetztige Uhrzeit fals du im Moment nicht weißt wie viel Uhr es ist ^^'\n"
                                 "/commands Zeigt dir in einer kurzen Beschreibung alles an was ich machen kann\n"
                                 "/help ... nun ja du hast es ja gerade genutzt ... also ja ... \n"
                                 "Versuch dich einfach etwas auszutoben, vielleicht antworte ich ja auch zu manchem ? ;D")
        elif Text == "/commands":
            self.sendMessage(ID, "/uhrzeit - Bekomme die Uhrzeit gesagt\n"
                                 "/commands - Siehe was ich schon alles kann!\n"
                                 "/help - HILFE ! Ich erkläre dir was ich alles machen kann ;)")

        else:
            self.sendMessage(ID, "Es tut mir leid aber ich habe dich nicht verstanden\n\nBeachte bitte!\nIch verstehe bis jetzt nur meine commands !")

    def sayHello(self, ID, UPDATE_ID):
        OLD_UP_ID = UPDATE_ID
        respond = False
        self.sendMessage(ID, "Hallo! Du bist Neu!\nKannst du mir deinen Namen verraten ?")
        timeout = int(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()).split(" ")[1].split(":")[2]) - int(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()).split(" ")[1].split(":")[2])
        last_update = self.lastUpdate(self.getUpdates_Json())
        NEW_UP_ID = self.getUpdateID(last_update)
        if OLD_UP_ID != NEW_UP_ID:
            if self.getID(last_update) == ID:
                respond = True
        while not respond  or timeout >= 10:
            timeout = int(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()).split(" ")[1].split(":")[2]) - timeout
            last_update = self.lastUpdate(self.getUpdates_Json())
            NEW_UP_ID = self.getUpdateID(last_update)
            if OLD_UP_ID != NEW_UP_ID:
                if self.getID(last_update) == ID:
                    respond = True
            time.sleep(0.2)
>>>>>>> a0185fc135c10f8bb0c8316b303f7b7eaa9a21b0
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

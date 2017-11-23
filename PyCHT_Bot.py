import json
import bs4 as bs
import urllib.request
import requests
import time
import threading



class Bot(object):
    def __init__(self):
        self.URL = "https://api.telegram.org/bot433782927:AAGhtZEFd6mx59OAHMiGROlV7R4_xgxILZI/"
        self.Conversations = self.loadConversations()
        self.NewContacts = []

    def start(self):
        LAST = self.lastUpdate(self.getUpdates_Json())
        UPDATE_ID_OLD = self.getUpdateID(LAST)
        while True:
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
        else:
            self.NewContacts.pop(self.NewContacts.index(ID))
            name = self.getText(ID, last_update)
            self.sendMessage(ID, "Hey "+name+"!\nDanke das du mit mir schreibst !\nSchaue dir die 'commands' an um mich zu bedienen :)\nDu kannst aber auch so mit mir schreiben nur bin ich noch sehr dumm!")
            self.writeNewContact(ID)
            self.Conversations = self.loadConversations()

    def writeNewContact(self, ID):
        data = open("Conversations.txt", "w")
        for i in self.Conversations:
            data.write(str(i)+"\n")
        data.write(str(ID)+"\n")
        data.close()

    def loadConversations(self):
        temp = []
        try:
            data = open("Conversations.txt", "r")
            data_lines = data.readlines()
            data.close()
            for i in data_lines:
                if i != "\n":
                    temp.append(int(i.split("\n")[0]))
            return temp

        except FileNotFoundError:
            print("ERROR FILE NOT FOUND")

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

    def getText(self, ID, update):
        if update["message"]["chat"]["id"] == ID:
            Text = update["message"]["text"]
            return Text
        else:
            return False

    def sendMessage(self, ID, text):
        args = {"chat_id" : ID, "text": text}
        result = requests.post(self.URL+"sendMessage", data=args)
        return result


if __name__ == "__main__":
    ActivateBot = Bot()
    ActivateBot.start()

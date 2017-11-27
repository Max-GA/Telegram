import json
import bs4 as bs
import urllib.request
import requests
from lxml import html
import time
import threading
import Profiles


class Bot(object):
    def __init__(self):
        self.Contacts = Profiles.Contacts()
        self.URL = "https://api.telegram.org/bot433782927:AAGhtZEFd6mx59OAHMiGROlV7R4_xgxILZI/"
        self.School_URL = "http://leibniz-pirmasens.de/vertretungsplan/vertretungklasse.html"
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
            elif self.getText(Result) == "/school":
                self.school(Chat_ID)
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

                    if Name == "Julia" or Name == "julia":
                        self.sendMessage(Chat_ID, "Btw, I think my father loves you\nHe is always talking and thinking about someone named 'Julia' ...\nBut I'm just a robot , what do I know ;)")

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

    def school(self, Chat_ID):
        if not self.Contacts.getSchool(Chat_ID):
            Result = self.lastUpdate(self.getUpdates_Json())
            Update_ID = self.getUpdateID(Result)

            self.sendMessage(Chat_ID, "Okay, before you can use this command I have to know somethings about you and your school!")
            self.sendMessage(Chat_ID, "At first I'm going to collect some information about your sujects and which grade your in.\nPlease answer the questions correctly\nIf you want to stop this setup , type /stop")
            self.sendMessage(Chat_ID, "So Please , which grade are you in ?\nA number would be great :)")

            grade_done = False
            first_courses = False
            rest_courses = False

            while not grade_done:
                new_Result = self.lastUpdate(self.getUpdates_Json())
                new_Update_ID = self.getUpdateID(new_Result)
                if new_Update_ID != Update_ID and self.getID(new_Result) == Chat_ID:
                    grade = self.getText(new_Result)
                    if grade != "/stop":
                        self.sendMessage(Chat_ID, "Okay {}, you are in the {} grade".format(self.Contacts.getName(Chat_ID), grade))
                        self.Contacts.setGrade(Chat_ID, grade)
                        Update_ID = new_Update_ID
                        grade_done = True
                    else:
                        self.sendMessage(Chat_ID, "You stopped the setup\nSorry to bother you")
                        self.Contacts.resetSchool(Chat_ID)
                        self.Update_ID = new_Update_ID
                        return False
            if int(self.Contacts.getGrade(Chat_ID)) > 10:
                self.sendMessage(Chat_ID, "Now I need your Advanced Courses\nPlease write them in the following format:\n\nCourse1 - Number(if important)\nCourse2\nCourse3 - Number(if important)\n...")
            else:
                self.sendMessage(Chat_ID, "Now I need our Main Courses\nPlease write them in the following format:\n\nCourse1 - Number(if important)\nCourse2\nCourse3 - Number(if important)\n...")
            while not first_courses:
                new_Result = self.lastUpdate(self.getUpdates_Json())
                new_Update_ID = self.getUpdateID(new_Result)
                if new_Update_ID != Update_ID and self.getID(new_Result) == Chat_ID:
                    courses = self.getText(new_Result)
                    if courses != "/stop":
                        if "\n" in courses:
                            self.sendMessage(Chat_ID, "Thanks! , Your courses are :")
                            temp = []
                            for course in courses.split("\n"):
                                if len(course.split("-")) > 1:
                                    if self.Contacts.shortCourse(Chat_ID, course.split("-")[0].replace(" ","")) != False:
                                        temp.append(self.Contacts.shortCourse(Chat_ID, course.split("-")[0].replace(" ",""))+course.split("-")[1].replace(" ",""))
                                    else:
                                        self.sendMessage(Chat_ID, "You inserted a course that is not in my database, please use only common subjects\nMaybe you also did a Typo , so please be careful when typing your courses\nI'm sorry but you have to do it again :(")
                                        self.Contacts.resetSchool(Chat_ID)
                                        self.Update_ID = new_Update_ID
                                        return False
                                else:
                                    if self.Contacts.shortCourse(Chat_ID, course) != False:
                                        temp.append(self.Contacts.shortCourse(Chat_ID, course))
                                    else:
                                        self.sendMessage(Chat_ID, "You inserted a course that is not in my database, please use only common subjects\nMaybe you also did a Typo , so please be careful when typing your courses\nI'm sorry but you have to do it again :(")
                                        self.Contacts.resetSchool(Chat_ID)
                                        self.Update_ID = new_Update_ID
                                        return False
                                self.sendMessage(Chat_ID, course)
                            self.Contacts.setMainCourses(Chat_ID, temp)
                            del temp
                            Update_ID = new_Update_ID
                            first_courses = True
                        else:
                            self.sendMessage(Chat_ID, "Wrong format ... Please try again")
                            Update_ID = new_Update_ID
                    else:
                        self.sendMessage(Chat_ID, "You stopped the setup\nSorry to bother you")
                        self.Contacts.resetSchool(Chat_ID)
                        self.Update_ID = new_Update_ID
                        return False
            self.sendMessage(Chat_ID, "The last things I need are your other courses\nSo now please again, tell me your different courses in the following format :\n\nCourse1 - Number(if important)\nCourse2\nCourse3 - Number(if important)\n...")
            while not rest_courses:
                new_Result = self.lastUpdate(self.getUpdates_Json())
                new_Update_ID = self.getUpdateID(new_Result)
                if new_Update_ID != Update_ID and self.getID(new_Result) == Chat_ID:
                    courses = self.getText(new_Result)
                    if courses != "/stop":
                        if "\n" in courses:
                            self.sendMessage(Chat_ID, "Thanks! , Your other courses are :")
                            temp = []
                            for course in courses.split("\n"):
                                if len(course.split("-")) > 1:
                                    if self.Contacts.shortCourse(Chat_ID, course.split("-")[0].replace(" ",""), False) != False:
                                        temp.append(self.Contacts.shortCourse(Chat_ID, course.split("-")[0].replace(" ",""))+course.split("-")[1].replace(" ",""))
                                    else:
                                        self.sendMessage(Chat_ID, "You inserted a course that is not in my database, please use only common subjects\nMaybe you also did a Typo , so please be careful when typing your courses\nI'm sorry but you have to do it again :(")
                                        self.Contacts.resetSchool(Chat_ID)
                                        self.Update_ID = new_Update_ID
                                        return False
                                else:
                                    if self.Contacts.shortCourse(Chat_ID, course, False) != False:
                                        temp.append(self.Contacts.shortCourse(Chat_ID, course))
                                    else:
                                        self.sendMessage(Chat_ID, "You inserted a course that is not in my database, please use only common subjects\nMaybe you also did a Typo , so please be careful when typing your courses\nI'm sorry but you have to do it again :(")
                                        self.Contacts.resetSchool(Chat_ID)
                                        self.Update_ID = new_Update_ID
                                        return False
                                self.sendMessage(Chat_ID, course)
                            self.Contacts.setOtherCourses(Chat_ID, temp)
                            del temp
                            Update_ID = new_Update_ID
                            rest_courses = True
                    else:
                        self.sendMessage(Chat_ID, "You stopped the setup\nSorry to bother you")
                        self.Contacts.resetSchool(Chat_ID)
                        self.Update_ID = new_Update_ID
                        return False
            self.sendMessage(Chat_ID, "Thank you , you finished the setup\nYou can use /school now to see which lessons are changed for the next day !")
            self.Update_ID = Update_ID
        else:

            page = html.fromstring(urllib.request.urlopen(self.School_URL + "?klasse=" + self.Contacts.getGrade(Chat_ID)).read())
            TITLE = page.xpath("//table//td")
            DATA = page.xpath("//table//td")
            start_var = 0
            INFORMATION = []

            # LOOP FOR MORE INFO IN TABLE , ALWAYS 7 STEPS
            # INFO IN TEXT
            # AUSGABE
            if len(DATA[0]) > 5:
                self.sendMessage(Chat_ID, "Important Information for this Day")
                self.sendMessage(Chat_ID, str(DATA[0].text))
                DATA.pop(DATA.index(DATA[0]))
                start_var = 1

            for i in range(0, len(DATA[start_var:]), 8):
                lesson_num = str(DATA[i].text)
                grade = str(DATA[i+1].text)
                lesson_nam = str(DATA[i+2].text)
                new_lesson = str(DATA[i+3].text)
                by_teacher = str(DATA[i+4].text)
                in_room = str(DATA[i+5].text)
                inplace_of = str(DATA[i+6].text)
                info = str(DATA[i+7].text)
                INFORMATION.append([lesson_num, grade, lesson_nam, new_lesson, by_teacher, in_room, inplace_of, info])


            self.sendMessage(Chat_ID, "Following information are affecting you")
            for row in INFORMATION:
                text = ""
                if row[2].upper() in self.Contacts.getCourses(Chat_ID):
                    if row[7] == "frei":
                        text = "Your subject {} is being cancelled in the {} lesson".format(row[2], row[0])
                    else:
                        if row[0] == 1:
                            text = text + """In the 1st lesson\n"""
                        elif row[0] == 2:
                            text = text + """In the 2nd lesson\n"""
                        elif row[0] == 3:
                            text = text + """In the 3rd lesson\n"""
                        else:
                            text = text + """In the {}th lesson\n""".format(row[0])

                        text = text + "Your subject {}".format(row[2])
                        if row[2] != row[3]:
                            text = text + " is replaced by {}".format(row[3])

                        text = text + " in room"

                        if row[5] != "---":
                            text = text + " {}".format(row[5])
                        else:
                            pass ### SCHAUE OB DIESER FALL ÜBERHAUPT EINTRIFFT

                        if row[4] != "---":
                            text = text + " with {} as the Teacher".format(row[4])

                        if row[6] != "&nbsp;":
                            text = text + "\nInstead of {}".format(row[6])

                        text = text + "\nInformation : {}".format(row[7])
                    self.sendMessage(Chat_ID, text)




        """
            In the 1st lesson\n
            Your subject g3 is replaced by e1 in room 301 with Ve as the Teacher
            Instead of g4
            Information : frei
        """

    def getUpdates_Json(self, clear = False):
        if clear:
            args = {"timeout": 100, 'offset': self.Update_ID+1}
        else:
            args = {"timeout": 100, 'offset': None}

        DATA = requests.get(self.URL+"getUpdates", data = args)
        if len(DATA.json()['result']) >= 90:
            self.getUpdates_Json(True)
        else:
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

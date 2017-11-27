import json
import pathlib
import sys

class Contacts(object):
    def __init__(self):
        if not pathlib.Path(sys.path[0]+"/Contacts.json").is_file():
            DATA = {}
            DATA['contacts'] = []
            self.setJson(DATA)

    def shortCourse(self, id, course, main=True):
        if course.upper() == "ENGLISCH" or course.upper() == "ENGLISH" or course.upper() == "E":
            return "E"
        elif course.upper() == "MATHE" or course.upper() == "MATHS" or course.upper() == "M":
            return "M"
        elif course.upper() == "DEUTSCH" or course.upper() == "GERMAN" or course.upper() == "D" or course.upper() == "DE":
            return "D"
        elif course.upper() == "FRANZÖSISCH" or course.upper() == "FRENCH" or course.upper() == "F" or course.upper() == "FRANZ":
            return "F"
        elif course.upper() == "ERDKUNDE" or course.upper() == "GEOGRAPHY" or course.upper() == "EK":
            if int(self.getGrade(id)) >= 11:
                if main:
                    return "Ek"
                else:
                    return "Eso"
            else:
                return "Ek"
        elif course.upper() == "SOZIALKUNDE" or course.upper() == "POLITICS" or course.upper() == "SOZ" or course.upper() == "SK":
            if int(self.getGrade(id)) >= 11:
                if main:
                    return "Sk"
                else:
                    return "Eso"
            else:
                return "Sk"
        elif course.upper() == "CEHMIE" or course.upper() == "CHEMISTRY" or course.upper() == "CH":
            if int(self.getGrade(id)) >= 7:
                return "Ch"
            else:
                return "Nw"
        elif course.upper() == "ETHIK" or course.upper() == "ETHIC" or course.upper() == "ET":
            return "Et"
        elif course.upper() == "RELIGION" or course.upper() == "RELIGION" or course.upper() == "RELI" or course.upper() == "R":
            return "R"
        elif course.upper() == "KATHOLISCH" or course.upper() == "CATHOLIC" or course.upper() == "KR":
            return "Kr"
        elif course.upper() == "EVANGELISCH" or course.upper() == "PROTESTANT" or course.upper() == "ER":
            return "Er"
        elif course.upper() == "KATHOLISCHERELIGION" or course.upper() == "CATHOLICRELIGION":
            return "Kr"
        elif course.upper() == "EVANGELISCHERELIGION" or course.upper() == "PROTESTANTRELIGION":
            return "Er"
        elif course.upper() == "BIOLOGIE" or course.upper() == "BIOLOGY" or course.upper() == "BIO" or course.upper() == "BI":
            if int(self.getGrade(id)) >= 7:
                return "Bi"
            else:
                return "Nw"
        elif course.upper() == "PHYSIK" or course.upper() == "PHYSICS" or course.upper() == "PH":
            if int(self.getGrade(id)) >= 7:
                return "ph"
            else:
                return "Nw"
        elif course.upper() == "MUSIK" or course.upper() == "MUSIC" or course.upper() == "MU":
            return "Mu"
        elif course.upper() == "KUNST" or course.upper() == "BILDENDEKUNST" or course.upper() == "ART" or course.upper() == "BK":
            return "Bk"
        elif course.upper() == "LATEIN" or course.upper() == "LATIN" or course.upper() == "L":
            return "L"
        elif course.upper() == "GESCHICHTE" or course.upper() == "HISTORY" or course.upper() == "G":
            return "G"
        elif course.upper() == "INFORMATIK" or course.upper() == "COMPUTERSCIENCE" or course.upper() == "INF" or course.upper() == "IN":
            if main:
                return "Inf"
            else:
                return "In"
        elif course.upper() == "SPORT" or course.upper() == "SPORTS" or course.upper() == "SP":
            return "Sp"
        elif course.upper() == "ESO":
            return "Eso"
        else:
            return False

    def getJson(self):
        with open("Contacts.json") as json_file:
            data = json.load(json_file)
            return data

    def setJson(self, data):
        with open("Contacts.json", "w") as json_file:
            json.dump(data, json_file)

    def newContact(self, name, id):
        DATA = self.getJson()
        DATA['contacts'].append(
            {
                'name': name,
                'id': id,
                'school': False
            }
        )
        self.setJson(DATA)

    def setGrade(self, id, grade):
        DATA = self.getJson()
        new_DATA = {}
        new_DATA['contacts'] = []
        for contact in DATA['contacts']:
            if contact['id'] == id:
                contact['school'] = True
                contact['grade'] = grade
            new_DATA['contacts'].append(contact)
        self.setJson(new_DATA)
    def getGrade(self, id):
        DATA = self.getJson()
        for contact in DATA['contacts']:
            if contact['id'] == id:
                return contact['grade']

    def getCourses(self, id):
        DATA = self.getJson()
        result = []
        for contact in DATA['contacts']:
            if contact['id'] == id:
                for main in range(0, len(contact['main_courses'])):
                    result.append(contact['main_courses']['{}_course'.format(main)].upper())
                for rest in range(0, len(contact['other_courses'])):
                    result.append(contact['other_courses']['{}_course'.format(rest)].upper())
        return result

    def setMainCourses(self, id, courses):
        DATA = self.getJson()
        new_DATA = {}
        new_DATA['contacts'] = []
        for contact in DATA['contacts']:
            if contact['id'] == id:
                contact['main_courses'] = {}
                for course_num in range(0, len(courses)):
                    contact['main_courses']['{}_course'.format(str(course_num))] = courses[course_num]
            new_DATA['contacts'].append(contact)
        self.setJson(new_DATA)

    def setOtherCourses(self, id, courses):
        DATA = self.getJson()
        new_DATA = {}
        new_DATA['contacts'] = []
        for contact in DATA['contacts']:
            if contact['id'] == id:
                contact['other_courses'] = {}
                for course_num in range(0, len(courses)):
                    contact['other_courses']['{}_course'.format(str(course_num))] = courses[course_num]
            new_DATA['contacts'].append(contact)
        self.setJson(new_DATA)


    def getSchool(self, id):
        DATA = self.getJson()
        for contact in DATA['contacts']:
            if contact['id'] == id:
                return contact['school']

    def resetSchool(self, id):
        DATA = self.getJson()
        new_DATA = {}
        new_DATA['contacts'] = []
        for contact in DATA['contacts']:
            if contact['id'] == id:
                contact['school'] = False
            new_DATA['contacts'].append(contact)
        self.setJson(new_DATA)

    def getName(self, id):
        DATA = self.getJson()
        for contact in DATA['contacts']:
            if contact['id'] == id:
                return contact['name']

    def getIDs(self):
        temp = []
        DATA = self.getJson()
        for contact in DATA['contacts']:
            temp.append(contact['id'])
        return temp
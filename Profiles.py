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
        if course == "Englisch" or course == "englisch" or course == "English" or course == "english":
            return "E"
        elif course == "Mathe" or course == "mathe" or course == "Maths" or course == "maths":
            return "M"
        elif course == "Deutsch" or course == "deutsch" or course == "German" or course == "german":
            return "D"
        elif course == "Französisch" or course == "französisch" or course == "French" or course == "french":
            return "F"
        elif course == "Erdkunde" or course == "erdkunde" or course == "Geography" or course == "geography":
            if int(self.getGrade(id)) >= 11:
                if main:
                    return "Ek"
                else:
                    return "Eso"
            else:
                return "Ek"
        elif course == "Sozialkunde" or course == "sozialkunde" or course == "Politics" or course == "politics":
            if int(self.getGrade(id)) >= 11:
                if main:
                    return "Sk"
                else:
                    return "Eso"
            else:
                return "Sk"
        elif course == "Chemie" or course == "chemie" or course == "Chemistry" or course == "chemistry":
            if int(self.getGrade(id)) >= 7:
                return "Ch"
            else:
                return "Nw"
        elif course == "Ethik" or course == "ethik" or course == "Ethics" or course == "ethics":
            return "Et"
        elif course == "Religion" or course == "Religion":
            return "R"
        elif course == "Biologie" or course == "biologie" or course == "Biology" or course == "biology":
            if int(self.getGrade(id)) >= 7:
                return "Bi"
            else:
                return "Nw"
        elif course == "Physik" or course == "physik" or course == "Physics" or course == "physics":
            if int(self.getGrade(id)) >= 7:
                return "ph"
            else:
                return "Nw"
        elif course == "Musik" or course == "musik" or course == "Music" or course == "music":
            return "Mu"
        elif course == "Kunst" or course == "kunst" or course == "Art" or course == "art":
            return "Bk"
        elif course == "Latein" or course == "latein" or course == "Latin" or course == "latin":
            return "L"
        elif course == "Geschichte" or course == "geschichte" or course == "History" or course == "history":
            return "G"
        elif course == "Informatik" or course == "informatik" or course == "Computer Science" or course == "computer science":
            if main:
                return "Inf"
            else:
                return "In"
        elif course == "Sport" or course == "sport" or course == "Sports" or course == "sports":
            return "Sp"
        elif course == "Eso" or course == "eso":
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
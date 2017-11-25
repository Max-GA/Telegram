import json
import pathlib
import sys

class Contacts(object):
    def __init__(self):
        if not pathlib.Path(sys.path[0]+"/Contacts.json").is_file():
            DATA = {}
            DATA['contacts'] = []
            self.setJson(DATA)

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
                'id': id
            }
        )
        self.setJson(DATA)

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
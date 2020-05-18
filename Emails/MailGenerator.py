import requests
import MySQLdb
import string
import random
import time
import json


class MailGenerator:
    def __init__(self):
        self.db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
        self.cursor = self.db.cursor()

    @staticmethod
    def GenerateEmail():
        first_name = json.load(open("firstnames.json", "r"))
        last_name = json.load(open("lastnames.json", "r"))
        first_name = first_name[random.randint(0, 299)]
        last_name = last_name[random.randint(0, 299)].capitalize()
        number = str(random.randint(500, 2000))
        suffix = '@dhosting.email'

        return first_name + "." + last_name + number + suffix

    @staticmethod
    def GeneratePassword():
        return ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for i in
                       range(random.randint(10, 15)))

    @staticmethod
    def CheckResponse(text):
        return text.split(', {"komunikaty":[')[1][1:32] == "E-mail account has been created"

    def InsertData(self, data):
        self.cursor.execute(
            "insert into 1swp_email_dhosting (Email, Password) values ('%s', '%s')" % (
                data[0], data[1]))
        self.db.commit()

    def CreateEmailAccount(self):
        data = [self.GenerateEmail(), self.GeneratePassword()]
        r = requests.post("https://panel.dhosting.com/poczta/a/dodaj-skrzynke/", data={
            "sign_key": "nvwuaf14J6ddcuRVgJ05KJJa1x4=",
            "adres_email": data[0],
            "password": data[1],
            "sms": "",
            "wartosc_wybrana": "2",
            "wartosc_wpisana": "2",
            "typ": [
                "brak",
                ""
            ],
            "filtr[spamassassin]": "T",
            "filtr[spf]": "T",
            "filtr[rbl]": "T",
            "wyszukiwarka_aliasow": "",
            "src_host": "",
            "src_login": "",
            "src_haslo": ""
        }, cookies={
            "dsid": "bd0404d5f3a7c7badf7e06a42e3920f2",
            "login": "michaelpyth"
        })
        if self.CheckResponse(r.text):
            self.InsertData(data)
            print("Added: " + str(data))
            return True
        else:
            print("Failed: " + str(data))
            return False

    def CreateEmails(self, accounts_to_create):
            for i in range(accounts_to_create):
                while not self.CreateEmailAccount():
                    pass


if __name__ == '__main__':
    i = MailGenerator()
    i.CreateEmails(accounts_to_create=100)

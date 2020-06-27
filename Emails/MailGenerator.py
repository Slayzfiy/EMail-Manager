from Emails.InfoGenerator import InfoGenerator as ig
from Emails.SQLManager import MySQLManager as sql
import requests
import string
import random
import json


class MailGenerator:
    def __init__(self):
        self.suffix = "@dhosting.email"
        self.sqlManager = sql("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
        self.ig = ig("firstnames.json", "lastnames.json", 5)

    def CreateHostAccount(self):
        name = "1234567890"
        while len(name) > 9:
            name = str(self.ig.GenerateFirstname()).lower() + str(self.ig.GenerateRandomNumber())
        email = self.ig.GenerateEmail("@gmail.com")
        password = self.ig.GeneratePassword()
        requests.post("https://dhosting.com/registration/koszyk.html", data={
            "_action": "dodajWyswietl", "RodzajUslugi": "glowna", "Operacja": "rejestracja",
             "NazwaWewnetrzna": "elastic", "Promocje[0][NazwaWewnetrzna]": "domena_za_1_zl",
             "Parametry[OkresRozliczeniowy]": "12"
        }, cookies={
            "hide-after-load": "yes", "PHPSESSID": "bf798196ae9e4b246602b174d37c6668"
        })
        response = requests.post("https://dhosting.com/registration/zamowienie2.html", data={
            "_action": "wyslij",
            "name": "",
            "dPanelLogin": name,
            "dPanelHaslo": password,
            "email": email,
            "zgodaDane": "T"
        }, cookies={
            "__cfduid": "da5234fc225d2d50368c22df423e909ad1593261478", "_fbp": "fb.1.1589747381705.1402120430",
             "_ga": "GA1.2.1888593612.1589747381", "_gid": "GA1.2.805262201.1593261477",
             "_hp2_id.1791626420": "{\"userId\":\"4101857338373244\",\"pageviewId\":\"1580577024557633\",\"sessionId\":\"195713887124829\",\"identity\":null,\"trackerVersion\":\"4.0\"}",
             "_hp2_ses_props.1791626420": "{\"r\":\"https://panel.dhosting.com/poczta/v/lista/\",\"ts\":1593285737875,\"d\":\"panel.dhosting.com\",\"h\":\"/billing/v/lista/wszystkie/\"}",
             "PHPSESSID": "bf798196ae9e4b246602b174d37c6668"
        }).text

        print(f"Creating account: Email: {email}\nName: {name}\nPassword: {password}")
        if json.loads(response)["Success"]:
            self.sqlManager.insertData("dhosting_host_accounts", "(Email, Name, Password)", [email, name, password])
            print("Account created")
        else:
            print(response)

    def GenerateEmail(self):
        firstname = self.firstnames[random.randint(0, 299)]
        lastname = self.lastNames[random.randint(0, 299)].capitalize()
        number = str(random.randint(10000, 99999))
        return firstname + "." + lastname + number + self.suffix

    @staticmethod
    def GeneratePassword():
        return ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase)
                       for i in range(random.randint(10, 15)))

    @staticmethod
    def CheckResponse(text):
        return text.split(', {"komunikaty":[')[1][1:32] == "E-mail account has been created"

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
            self.sqlManager.insertData("1swp_email_dhosting", "(Email, Password)", data)
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
    i.CreateHostAccount()

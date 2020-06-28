from Emails.InfoGenerator import InfoGenerator as ig
from Emails.SQLManager import MySQLManager as sql
from bs4 import BeautifulSoup
import requests
import json
import time


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

        if json.loads(response)["Success"]:
            self.sqlManager.insertData("dhosting_host_accounts", "(Email, Name, Password)", [email, name, password])
            print(f"Host-Account created ({email}).")

    def GetLatestHostAccount(self):
        return self.sqlManager.getData("dhosting_host_accounts", "Name", "order By Created desc limit 1")[0]

    def GetdsID(self, account):
        r = requests.post("https://panel.dhosting.com/", data={
            "logowanie": "true",
            "logowanie_username": account[1],
            "logowanie_password": account[2]
        })
        return r.cookies["dsid"]

    @staticmethod
    def SendCreateRequest(email, password, dsid, hostName):
        print(f"Creating Email-Account ({email}) using Host: {hostName}")
        requests.post("https://panel.dhosting.com/poczta/a/dodaj-skrzynke/", data={
            "sign_key": "nvwuaf14J6ddcuRVgJ05KJJa1x4=",
            "adres_email": email,
            "password": password,
            "sms": "",
            "wartosc_wybrana": "2",
            "wartosc_wpisana": "2",
            "typ":
                [
                    "wlasny",
                    ""
                ],
            "wyszukiwarka_aliasow": "",
            "src_host": "",
            "src_login": "",
            "src_haslo": ""
        }, cookies={
            "dsid": dsid,
            "login": hostName,
        })

    def CreateEmailAccount(self, hostAccount, dsid):
        emailAccount = [self.ig.GenerateEmail("@dhosting.email"), self.ig.GeneratePassword()]
        self.SendCreateRequest(emailAccount[0], emailAccount[1], dsid, hostAccount)
        self.sqlManager.insertData("dhosting_email_accounts", "(Email, Password)", emailAccount)

    def DeleteEmailAccounts(self):
        hostAccount = self.GetLatestHostAccount()
        dsid = self.GetdsID(hostAccount)
        for account in self.sqlManager.getData("dhosting_email_accounts", "Email, Password"):
            r = requests.get(f"https://panel.dhosting.com/poczta/jv/form-usun-adres/{account[0]}/", cookies={
                "dsid": dsid,
                "login": hostAccount[1],
            })

            first = r.text.split('<input type="hidden" name="')[1].split('" value="')[0]
            second = r.text.split(f'<input type="hidden" name="{first}" value="')[1].split('" />')[0]
            requests.post("https://panel.dhosting.com/poczta/a/usun-adres//", data={
                first: second
            }, cookies={
                "dsid": dsid,
                "login": hostAccount[1],
            })
            print(f"Deleted {account[0]}")


if __name__ == '__main__':
    mode = "d"
    generator = MailGenerator()
    if mode == "c":
        hostAccount = generator.GetLatestHostAccount()
        dsid = generator.GetdsID(hostAccount)
        for index in range(10):
            generator.CreateEmailAccount(hostAccount, dsid)
            time.sleep(3)
    elif mode == "d":
        generator.DeleteEmailAccounts()

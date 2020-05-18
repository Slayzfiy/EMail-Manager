import requests
import concurrent.futures
import json
import random
import string
import MySQLdb


class MailGenerator:
    def __init__(self):
        self.db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
        self.cursor = self.db.cursor()

    @staticmethod
    def Fetch_Email():
        first_name = json.load(open("firstnames.json", "r"))
        last_name = json.load(open("lastnames.json", "r"))
        first_name = first_name[random.randint(0, 299)]
        last_name = last_name[random.randint(0, 299)].capitalize()
        number = str(random.randint(500, 2000))
        suffix = '@dhosting.email'

        return first_name + last_name + number + suffix

    @staticmethod
    def Fetch_Password():
        return ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for i in
                       range(random.randint(10, 15)))

    def Insert_data(self, data):
        self.cursor.execute(
            "insert into 1swp_email_dhosting (Email, Password) values ('%s', '%s')" % (
                data[0], data[1]))
        self.db.commit()

    def CreateMailsTemplate(self, URLS):
        email = self.Fetch_Email()
        password = self.Fetch_Password()

        r = requests.post("https://panel.dhosting.com/poczta/a/dodaj-skrzynke/", data={
            "sign_key": "nvwuaf14J6ddcuRVgJ05KJJa1x4=",
            "adres_email": email,
            "password": password,
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
        data = [email, password]
        self.Insert_data(data)
        print(data)

    def Create_Mails(self, account_to_create):
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            URL = ['https://panel.dhosting.com/poczta/a/dodaj-skrzynke/']
            future_to_url = {executor.submit(self.CreateMailsTemplate, URL): URL for x in range(account_to_create)}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                except Exception as ex:
                    print(ex)


if __name__ == '__main__':
    i = MailGenerator()
    i.Create_Mails(account_to_create=100)

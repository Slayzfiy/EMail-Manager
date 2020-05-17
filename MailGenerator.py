import requests
from urllib.request import Request, urlopen
import requests
import concurrent.futures
import json
import random
import string


class MailGenerator:
    def __init__(self):
        pass

    def Fetch_Email(self):
        first_name = json.load(open("firstnames.json", "r"))
        last_name = json.load(open("lastnames.json", "r"))
        first_name = first_name[random.randint(0, 299)]
        last_name = last_name[random.randint(0, 299)].capitalize()
        number = str(random.randint(500, 2000))
        suffix = '@dhosting.email'

        return first_name + last_name + number + suffix

    def Fetch_Password(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for i in
                       range(random.randint(10, 15)))

    def CreateEmail(self, URLS):
        r = requests.post("https://panel.dhosting.com/poczta/a/dodaj-skrzynke/", data={
            "sign_key": "nvwuaf14J6ddcuRVgJ05KJJa1x4=",
            "adres_email": self.Fetch_Email(),
            "password": self.Fetch_Password(),
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
            "dsid": "c4ed4afbfaad8d8e57db1514ffc1cce4",
            "login": "michaelpyth"
        })


    def Products_With_Relevance(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            # Start the load operations and mark each future with its URL
            URL = ['https://panel.dhosting.com/poczta/a/dodaj-skrzynke/']
            future_to_url = {executor.submit(self.CreateEmail, URL): URL for x in range(100)}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                data = future.result()


if __name__ == '__main__':
    i = MailGenerator()
    i.Products_With_Relevance()




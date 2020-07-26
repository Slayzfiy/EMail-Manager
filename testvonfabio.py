from Tools.InfoGenerator import InfoGenerator as ig
from Tools.SQLManager import MySQLManager as sql
import requests
import json
import time


class PostRequests:
    def __init__(self):
        pass

    def Post(self):
        session = requests.Session()
        session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        ref = "https://gleam.io/EDJt6/gewinnspiel-chromebooks-juli-2020"
        headers = {"Referer": ref}

        post_infos = {
            "campaign_key": "EDJt6",
            "additional_details": "True",
            "contestant": {
                "firstname": "fabio",
                "lastname": "kreis",
                "land": "Österreich",
                "hiermit_akzeptiere_ich_die_teilnahmebedingungen": "True",
                "email": "asdafasf123ssdfjkl@gmail.com"
            }
        }
        r = session.post("https://gleam.io/set-contestant", json=post_infos, headers=headers)

        print("1.")
        print(r.text + "\n")
        print(str(r.cookies) + "\n")

        header = session.headers
        cookies = requests.utils.dict_from_cookiejar(session.cookies)

        print('header', header)
        print('cookies', cookies)

        response = session.post("https://gleam.io/enter/EDJt6/5018511", headers=header, cookies=cookies).text
        print(response)


if __name__ == "__main__":
    i = PostRequests()
    i.Post()
    input()

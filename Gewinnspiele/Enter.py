import requests
import MySQLdb


class Enter:
    def __init__(self):
        self.db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
        self.cursor = self.db.cursor()
        pass

    def GetEmailAdresses(self):
        self.cursor.execute("select Email from 1swp_email_dhosting")
        data = []
        for line in self.cursor.fetchall():
            data.append(line[0])
        return data

    def SendPostRequest(self, url, data, cookies):
        response = requests.post(url, data=data, cookies=cookies)
        return response


if __name__ == "__main__":
    enter = Enter()
    adresses = enter.GetEmailAdresses()
    for email in adresses:
        data = {
            "dynamic_form[anrede]" : "0",
            "dynamic_form[vorname]": "vorname",
            "dynamic_form[nachname]": "nachname",
            "dynamic_form[adresse]": "adresse",
            "dynamic_form[plz]": "1000",
            "dynamic_form[ort]": "ort",
            "dynamic_form[tel]": "64564654",
            "dynamic_form[geburtsdatum]": "11.11.1990",
            "dynamic_form[email]": email,
            "dynamic_form[1528366991805a]": "1",
            "dynamic_form[_token]": "5yly9RMh0bUCOIVxUBson95r58FzehtEbz81qJ2TbZg"
        }
        cookies = {

        }
        print(enter.SendPostRequest("https://www.willi.aka.krone.at/missions/1b17bdd2dbd3fbc1/validate", data, cookies))
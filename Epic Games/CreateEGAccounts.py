from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


import MySQLdb
import random
import time
import json
import string


db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
cursor = db.cursor()


def getEmail():
    cursor.execute(
        "select Email from 1swp_email_dhosting where HasGTAV = 'No' and Status = 'Nothing' limit 1")
    return cursor.fetchone()


def insertAccount(data):
    cursor.execute(
        "insert into 1swp_eg_accounts (Country, Firstname, Lastname, Username, Email, Password, Status) values('%s', '%s', '%s', '%s', '%s', '%s', 'Waiting')" % (
        data[0], data[1], data[2], data[3], data[4], data[5]))
    cursor.execute("update 1swp_email_dhosting set Status = 'Waiting' where Email = '%s'" % data[4])
    db.commit()
    return


def getCountry():
    return json.load(open("countries.json", "r"))["countries"][random.randint(0, 228)]["name"]


def getFirstname():
    return json.load(open("firstnames.json", "r"))[random.randint(0, 299)]


def getLastname():
    return str(json.load(open("lastnames.json", "r"))[random.randint(0, 299)]).capitalize()


def getUsername(firstname):
    return firstname + "".join((str(random.randint(0, 9)) for i in range(15 - len(str(firstname)))))


def getPassword():
    return "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(15))


class Registration:
    def __init__(self):
        self.email = getEmail()[0]

        self.country = str(getCountry())
        self.firstname = str(getFirstname())
        self.lastname = str(getLastname())
        self.username = str(getUsername(self.firstname))
        self.password = str(getPassword())

        self.data = [self.country, self.firstname, self.lastname, self.username, self.email, self.password]

        self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--headless")
        self.driver = webdriver.Chrome("chromedriver.exe", options=self.options)
        self.driver.set_window_size(769, 899)


    def register(self):
        self.driver.get("https://www.epicgames.com/id/register")
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "react-select-2-input"))).send_keys(self.country + Keys.ENTER)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "name"))).send_keys(self.firstname)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "lastName"))).send_keys(self.lastname)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "displayName"))).send_keys(self.username)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "email"))).send_keys(self.email)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "password"))).send_keys(self.password)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "termsOfService"))).click()
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "btn-submit"))).click()

        print("email sent to %s" % self.email)
        insertAccount(self.data)

        try:
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "code")))
        except:
            print("da")


if __name__ == "__main__":
    numAccounts = 1

    for i in range(numAccounts):
        reg = Registration()
        reg.register()
        time.sleep(1000)
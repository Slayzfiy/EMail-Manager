from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


import MySQLdb
import random
import time
import json
import re


db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
cursor = db.cursor()


def getData():
    cursor.execute(
        "select Firstname, Lastname, Email, Password from 1swp_email_accounts where HasGTAV = 0 limit 1")
    data = cursor.fetchone()
    return data


def update(email):
    cursor.execute(
        "update 1swp_email_accounts set HasGTAV = 1 where Email = '%s'" % email)
    db.commit()
    return


def getCountry():
    return json.load(open("countries.json", "r"))["countries"][random.randint(0, 238)]["name"]


class Registration:
    def __init__(self):
        self.data = getData()

        self.country = str(getCountry())
        self.firstname = str(self.data[0])
        self.lastname = str(''.join([i for i in self.data[1] if not i.isdigit()]))
        self.username = self.getName()
        self.email = self.data[2]
        self.password = self.data[3]

        self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--headless")
        self.driver = webdriver.Chrome("chromedriver.exe", options=self.options)
        self.driver.set_window_size(769, 899)
        pass

    def getName(self):
        return self.firstname + "".join((str(random.randint(0, 9)) for i in range(15 - len(str(self.firstname)))))

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

        print("email sent to %s" % (self.email))

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
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


def getEmail():
    db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
    cursor = db.cursor()
    cursor.execute(
        "select Email from 1swp_email_dhosting where GTAV = 'No' limit 1")
    db.close()
    return cursor.fetchone()


def insertAccount(data):
    db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
    cursor = db.cursor()
    cursor.execute(
        "insert into 1swp_eg_accounts (Country, Firstname, Lastname, Username, Email, Password, Status) values('%s', '%s', '%s', '%s', '%s', '%s', 'Waiting')" % (
        data[0], data[1], data[2], data[3], data[4], data[5]))
    db.commit()
    db.close()
    return


def updateAccount(email, status):
    db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
    cursor = db.cursor()
    cursor.execute("update 1swp_eg_accounts set Status = '%s' where Email = '%s'" % (status, email))
    db.commit()
    db.close()
    return


def deleteAccount(email):
    db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
    cursor = db.cursor()
    cursor.execute("delete from 1swp_eg_accounts where Email = '%s'" % email)
    cursor.execute("update 1swp_email_dhosting set GTAV = 'Failed' where Email = '%s'" % email)
    db.commit()
    db.close()
    return


def getFirstname():
    return json.load(open("firstnames.json", "r"))[random.randint(0, 299)]


def getLastname():
    return str(json.load(open("lastnames.json", "r"))[random.randint(0, 299)]).capitalize()


def getUsername(firstname):
    return firstname + "".join((str(random.randint(0, 9)) for i in range(15 - len(str(firstname)))))


def getPassword():
    return "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(14)) + "1"


def getCode(email, type):
    db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
    cursor = db.cursor()
    cursor.execute(
        "select %s from 1swp_eg_accounts where Email = '%s'" % (type, email))
    db.close()
    return cursor.fetchone()[0]


def confirmAccount(email):
    db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
    cursor = db.cursor()
    cursor.execute(
        "update 1swp_email_dhosting set GTAV = 'YES' where Email = '%s'" % email)
    db.close()


class Registration:
    def __init__(self):
        self.email = getEmail()[0]

        self.country = "United States"
        self.firstname = str(getFirstname())
        self.lastname = str(getLastname())
        self.username = str(getUsername(self.firstname))
        self.password = str(getPassword())
        self.data = [self.country, self.firstname, self.lastname, self.username, self.email, self.password]

    def register(self):
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        driver = webdriver.Chrome("chromedriver.exe", options=options)
        driver.set_window_size(500, 980)
        driver.get("https://www.epicgames.com/id/register")
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "react-select-2-input"))).send_keys(self.country + Keys.ENTER)
        time.sleep(1)
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "name"))).send_keys(self.firstname)
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "lastName"))).send_keys(self.lastname)
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "displayName"))).send_keys(self.username)
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "email"))).send_keys(self.email)
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "password"))).send_keys(self.password)
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "termsOfService"))).click()
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "btn-submit"))).click()

        try:
            codeElement = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "code")))
        except:
            print("%s crashed because of CAPTCHA." % self.email)
            driver.close()
            return "ERROR_CAPTCHA"
        try:
            insertAccount(self.data)
            print("Email sent to %s" % self.email)
            code = ""
            while code == "":
                code = str(getCode(self.email, "Code1"))
                time.sleep(2)

            updateAccount(self.email, "Nothing")
            codeElement.send_keys(str(code))

            driver.find_element_by_id("continue").click()
            time.sleep(5)
            driver.get("https://www.epicgames.com/account/password?from=webPDP&lang=de#2fa-signup")
            codeElement = ""
            while codeElement == "":
                try:
                    WebDriverWait(driver, 3).until(ec.presence_of_element_located(
                        (By.XPATH, "//button[contains(text(), 'Authentifizierung per E-Mail aktivieren')]"))).click()
                    codeElement = WebDriverWait(driver, 2).until(ec.presence_of_element_located((By.NAME, "challengeEmailCode")))
                except:
                    pass
            codeElement.click()
            updateAccount(self.email, "Waiting")
            code = ""
            while code == "":
                code = str(getCode(self.email, "Code2"))
                time.sleep(1)
            codeElement.send_keys(str(code))
            updateAccount(self.email, "Nothing")
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//button[contains(text(), 'fortfahren')]"))).click()
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Fertig')]"))).click()
            driver.get("https://www.epicgames.com/store/de/product/grand-theft-auto-v/home")
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Fortfahren')]"))).click()
            WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Holen')]"))).click()
            time.sleep(4)
            driver.execute_script('document.getElementsByClassName("btn btn-primary")[0].click()')
            print("Account %s finished. Restarting now." % self.email)
            time.sleep(3)
            driver.get("https://www.epicgames.com/account/password")
            WebDriverWait(driver, 3).until(ec.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Authentifizierung per E-Mail deaktivieren')]"))).click()
            time.sleep(1)
            WebDriverWait(driver, 5).until(ec.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Fortfahren')]"))).click()
            time.sleep(3)
            driver.close()
            return "SUCCESS"
        except Exception as e:
            print("Crashed because of: " + str(e))
            deleteAccount(self.email)
            driver.close()


if __name__ == "__main__":
    numAccounts = 10

    for i in range(numAccounts):
        reg = Registration()
        errorCode = ""
        while errorCode != "SUCCESS":
            errorCode = reg.register()

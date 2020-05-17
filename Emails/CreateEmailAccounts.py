from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

import urllib.request
import pytesseract
import cv2

import datetime
import MySQLdb
import random
import string
import time
import json
import os


db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
cursor = db.cursor()
pytesseract.pytesseract.tesseract_cmd = "C://Program Files//Tesseract-OCR//tesseract.exe"


def fixCookies(driver):
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(
        (By.XPATH, "//button[@class='lg-cc__button lg-cc__button_type_action']"))).click()
    return


def getData():
    prefix = "@yandex.com"
    firstnames = json.load(open("firstnames.json", "r"))
    lastnames = json.load(open("lastnames.json", "r"))

    firstname = firstnames[random.randint(0, 299)]
    lastname = lastnames[random.randint(0, 299)].capitalize()
    number = str(random.randint(100000, 999999))
    email = "%s.%s%s%s" % (firstname, lastname, number, prefix)
    musician = "%s %s" % (firstnames[random.randint(0, 299)], lastnames[random.randint(0, 299)].capitalize())
    password = "".join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for i in
                       range(random.randint(10, 15)))
    data = [firstname, lastname, number, email, password, musician]
    return data


def insertUser(data):
    cursor.execute(
        "insert into 1swp_email_accounts (Firstname, Lastname, Number, Email, Password, Musician) values ('%s', '%s', '%s', '%s', '%s', '%s')" % (
            data[0], data[1], data[2], data[3], data[4], data[5]))
    db.commit()


def getText(imageLink):
    randomNumber = random.randint(0, 1000000000)
    path = (str(randomNumber) + "captcha_image.jpg")

    urllib.request.urlretrieve(imageLink, path)
    image = cv2.imread(path)
    height, width = image.shape[:2]

    imageLeft = image[0:height, 0:int(width / 2)]
    imageRight = image[0:height, int(width / 2):width]

    text1 = pytesseract.image_to_string(imageLeft, config='--oem 3 --psm 6')
    text2 = pytesseract.image_to_string(imageRight, config='--oem 3 --psm 6')
    os.remove((os.getcwd() + "//" + path))
    return text1.replace("\n", "") + text2.replace("\n", "")


def login(driver):
    try:
        data = getData()

        firstnameField = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//input[@id='firstname']")))
        firstnameField.send_keys(data[0])
        driver.find_element_by_id("lastname").send_keys(data[1])
        driver.find_element_by_id("login").send_keys(data[0] + "." + data[1] + str(data[2]))
        driver.find_element_by_id("password").send_keys(data[4])
        driver.find_element_by_id("password_confirm").send_keys(data[4])

        driver.find_element_by_xpath("//span[@class='toggle-link link_has-no-phone']").click()
        WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.ID, "hint_answer"))).send_keys(data[5])

        while True:
            captchaText = ""
            while captchaText == "":
                divElement = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, "//div[@class='captcha__reload']")))
                divElement.click()
                time.sleep(0.5)
                image = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, "//img[@class='captcha__image']")))
                imageLink = image.get_attribute("src")

                captchaText = getText(imageLink)

            captchaField = driver.find_element_by_id("captcha")
            captchaField.send_keys(captchaText)
            driver.find_element_by_xpath("//div[@class='form__submit']").click()

            try:
                WebDriverWait(driver, 5).until(
                    ec.presence_of_element_located((By.XPATH, "//div[@class='t-eula-accept']/button[1]"))).click()
            except:
                return

            try:
                WebDriverWait(driver, 5).until(
                    ec.presence_of_element_located((By.XPATH, "//div[@class='reg-field__popup']")))
                for i in range(20):
                    captchaField.send_keys(Keys.BACK_SPACE)
            except:
                insertUser(data)
                WebDriverWait(driver, 10).until(ec.presence_of_element_located(
                    (By.XPATH, "//a[starts-with(@href, '/passport?origin=passport_profile&')]"))).click()
                time.sleep(2)
                driver.execute_script(
                    'document.getElementsByClassName("control button2 button2_view_classic button2_size_m button2_theme_action button2_type_link")[0].click()')
                print("User %s confirmed!" % (data[0] + "." + data[1] + str(data[2])))
                return
    except Exception as ex:
        print("Crashed because of " + str(ex).replace("\n", "", -1))


options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome("chromedriver.exe", options=options)
driver.get("https://passport.yandex.com/registration")
fixCookies(driver)
driver.set_window_size(769, 899)

while True:
    driver.get("https://passport.yandex.com/registration")
    login(driver)

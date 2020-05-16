from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import MySQLdb
import time


def getData(cursor):
    cursor.execute("select Firstname, Lastname, Number, Email, Password, Musician from 1swp_email_accounts_yandex where Type = 'Unconfirmed' limit 1")
    return cursor.fetchone()


def login(driver):
    firstnameField = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "//input[@id='firstname']")))

    firstnameField.send_keys(firstname)
    driver.find_element_by_id("lastname").send_keys(lastname)
    driver.find_element_by_id("login").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("password_confirm").send_keys(password)

    driver.find_element_by_xpath("//span[@class='toggle-link link_has-no-phone']").click()
    driver.find_element_by_id("hint_answer").send_keys(musician)

    image = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//img[class='captcha__image']")))

    print(image.get_attribute("src"))



def getConfirmationEmail(db, cursor):
    cursor.execute("select Email from 1swp_email_accounts where Type = 'Confirmed' order by ID desc limit 1")
    email = cursor.fetchone()[0]
    cursor.execute("update 1swp_email_accounts set Type = 'Waiting' where Email = '%s'" % email)
    db.commit()
    return email


db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
cursor = db.cursor()
data = getData(cursor)
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/micha/AppData/Local/Google/Chrome/User Data/Default")
numAccounts = 1

for i in range(numAccounts):
    firstname = data[0]
    lastname = data[0]
    username = data[0] + "." + data[1] + str(data[2])
    password = data[4]
    musician = data[5]

    driver = webdriver.Chrome("chromedriver.exe", options=options)
    driver.set_window_size(769, 899)
    driver.get("https://passport.yandex.com/registration")
    login(driver)

    time.sleep(100)
    if hasCaptcha(driver):
        pass
    elif hasEmail(driver):
        confirmationEmail = getConfirmationEmail(db, cursor)
        driver.find_element_by_xpath("//div[@class='humanVerification-block-email']").click()
        driver.find_element_by_id("emailVerification").send_keys(confirmationEmail)
        driver.find_elements_by_class_name("pm_button primary codeVerificator-btn-send")[0].click()
        print(confirmationEmail)

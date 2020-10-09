from Tools.SQLManager import MySQLManager
from Tools.InfoGenerator import InfoGenerator
from Tools.TestmailQuery import Query

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver

import socket
import requests
import time
import re


class Generator:
    def __init__(self):
        self.testmailHeader = {"Authorization": "Bearer 25ad9e51-ce4d-4bcb-b15f-b8dbd2779ca0"}

    def Setup(self, proxy="", headless=False):
        chrome_options = webdriver.ChromeOptions()

        if proxy != "":
            chrome_options.add_argument('--proxy-server=' + proxy)
        if headless:
            chrome_options.add_argument("--headless")

        if "127" in str(socket.gethostbyname(socket.gethostname())):
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome("../../Files/chromedriver.exe", options=chrome_options)

    def Destroy(self):
        self.driver.close()

    def Start(self, sqlManager, infoGenerator, query):
        info = [infoGenerator.GenerateEmail("protonmail"), infoGenerator.GeneratePassword()]
        print(f"Creating {info[0]} using Password: '{info[1]}'")

        self.driver.get("https://mail.protonmail.com/create/new?language=en")

        # Enter Username
        registrationForm = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//iframe[@class='top']")))
        self.driver.switch_to.frame(registrationForm)
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//input[@id='username']"))).send_keys(info[0])
        self.driver.switch_to.default_content()

        # Enter Password
        self.driver.find_element(By.XPATH, "//input[@id='password']").send_keys(info[1])
        self.driver.find_element(By.XPATH, "//input[@id='passwordc']").send_keys(info[1])

        # Enter Recovery Email
        recoveryEmail = infoGenerator.GenerateEmail("testmail")
        submitForm = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//iframe[@class='bottom']")))
        self.driver.switch_to.frame(submitForm)
        self.driver.find_element(By.XPATH, "//input[@id='notificationEmail']").send_keys(recoveryEmail)

        # Submit Account
        self.driver.find_element(By.XPATH, "//button[@name='submitBtn']").click()

        # Verify Email
        verificationPanel = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//div[@id='verification-panel']")))
        elements = verificationPanel.find_elements(By.XPATH, "./div")
        for element in elements:
            if element.get_attribute("class") == "humanVerification-block-email" and False:
                element.find_element(By.XPATH, ".//input[@id='id-signup-radio-email']").click()
                verificationPanel.find_element(By.XPATH, ".//input[@id='emailVerification']").send_keys(recoveryEmail)
                verificationPanel.find_element(By.XPATH,
                                               ".//button[contains(@class, 'codeVerificator-btn-send')]").click()

                print("Checking")
                tag = recoveryEmail.split(".")[1].split("@")[0]
                response = query.getEmailBody(tag)
                code = re.search("\d+", response).group(0)
                print(code)
                print("Done")
                time.sleep(1000)
                break
        # sqlManager.insertData("protonmail_email_accounts", "(Email, Password)", info)


if __name__ == "__main__":
    infoGenerator = InfoGenerator()
    sqlManager = MySQLManager("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
    query = Query()

    gen = Generator()
    gen.Setup()
    gen.Start(sqlManager, infoGenerator, query)
    gen.Destroy()

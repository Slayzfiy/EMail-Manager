from Tools.SQLManager import MySQLManager
from Tools.InfoGenerator import InfoGenerator
from Tools.TestmailQuery import Query
from Tools.ProxyGenerator import OwnProxies as pr

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

import socket
import requests
import time
import re


class Bot:
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

    def Start(self, infoGenerator, sqlManager):
        info = [infoGenerator.GenerateFirstname(), infoGenerator.GenerateEmail("testmail")]

        self.driver.get("https://basic-tutorials.de?rpid=60&rpr=121493")
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="rafflepress-login-email"]/button'))).click()
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="name"]'))).send_keys(info[0])
        self.driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(info[1])
        self.driver.find_element(By.XPATH, '//*[@id="rafflepress-giveaway-login"]/div/div[2]/div[1]/button').click()

        time.sleep(1000)


if __name__ == "__main__":
    infoGenerator = InfoGenerator()
    sqlManager = MySQLManager("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
    proxy = pr()
    proxies = proxy.GetProxies()

    bot = Bot()
    bot.Setup()
    bot.Start(infoGenerator, sqlManager)
    bot.Destroy()
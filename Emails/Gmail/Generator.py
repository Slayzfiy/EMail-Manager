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

    def Start(self, sqlManager, infoGenerator):
        info = [infoGenerator.GenerateEmail("protonmail"), infoGenerator.GeneratePassword()]
        print(f"Creating {info[0]} using Password: '{info[1]}'")

        self.driver.get("https://accounts.google.com/signin/v2")
        time.sleep(10000)
        actions = ActionChains(self.driver)
        for i in range(4):
            actions.send_keys(Keys.TAB)
        actions.perform()
        time.sleep(1000)


if __name__ == "__main__":
    infoGenerator = InfoGenerator()
    sqlManager = MySQLManager("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")

    proxy = pr()
    proxies = proxy.GetProxies()

    gen = Generator()
    gen.Setup(proxies[0])
    gen.Start(sqlManager, infoGenerator)
    gen.Destroy()

from Giveaways.GiveawayManager import GivawayManager
from Tools.InfoGenerator import InfoGenerator
from Tools.ProxyGenerator import *

from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import socket


class Gleam:
    def __init__(self):
        self.fieldNames = ["firstname", "lastname", "email", "land", "hiermit_akzeptiere_ich_die_teilnahmebedingungen"]
        self.driver = None

    def Setup(self, proxy):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=' + proxy)
        chrome_options.add_argument("--headless")

        if str(socket.gethostbyname(socket.gethostname())) == "192.168.8.182":
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome("../Files/chromedriver.exe", options=chrome_options)

    def Destroy(self):
        self.driver.close()

    def HandleElement(self, element, info):
        for fieldName in self.fieldNames:
            if fieldName in str(element.get_attribute("ng-class")) or fieldName in str(
                    element.get_attribute("ng-init")):
                inputField = element.find_element(By.XPATH, f".//*[@name='{fieldName}']")
                if fieldName == self.fieldNames[0]:
                    inputField.send_keys(info[0])
                elif fieldName == self.fieldNames[1]:
                    inputField.send_keys(info[1])
                elif fieldName == self.fieldNames[2]:
                    inputField.send_keys(info[2])
                elif fieldName == self.fieldNames[3]:
                    inputField.send_keys("Ö")
                elif fieldName == self.fieldNames[4]:
                    element.find_element(By.XPATH, ".//label[@class='checkbox']").click()

    def Start(self, url, info):
        try:
            self.driver.delete_all_cookies()
            self.driver.get(url)

            for j in range(10):
                fieldsets = self.driver.find_elements(By.XPATH, "//fieldset[@class='inputs']")
                for fieldset in fieldsets:
                    if fieldset.is_displayed():
                        container = fieldset.find_element(By.XPATH, ".//div[contains(@class, 'contestant-form-group')]")
                        elements = container.find_elements(By.XPATH, "./div")
                        for element in elements:
                            self.HandleElement(element, info)

                        # Click on Submit
                        time.sleep(1)
                        self.driver.find_elements(By.XPATH, "//button[@ng-click='setContestant()']")[0].click()

                        # Wait for Response
                        element = self.driver.find_element_by_class_name("tally")
                        for i in range(40):
                            status = element.get_attribute("uib-tooltip")
                            if "Deine Teilnahme am Gewinnspiel ist bestätigt" in status:
                                return True
                            elif "Du erstellst zu viele Einträge." in status:
                                return False
                            time.sleep(0.1)
                time.sleep(0.5)
            return False
        except:
            return False


if __name__ == "__main__":
    print("test")
    proxies = OwnProxies().GetProxies()

    infoGenerator = InfoGenerator()
    manager = GivawayManager()
    giveaways = manager.GetOpenGiveaways()
    gleam = Gleam()

    if len(giveaways) > 0:
        while True:
            for giveaway in giveaways:
                url = giveaway[1]
                id = giveaway[0]
                counter = 0
                proxyCounter = 0
                for proxy in proxies:
                    proxyCounter += 1
                    print(f"{proxyCounter}. Using Proxy {proxy}")
                    gleam.Setup(proxy)
                    for i in range(21):
                        info = [infoGenerator.GenerateFirstname(), infoGenerator.GenerateLastname(), infoGenerator.GenerateEmail("testmail")]
                        if gleam.Start(url, info):
                            counter += 1
                            print(f"{counter}. Entered {info[2]}")
                            manager.EnterEmailAccount(info[2], id)
                        else:
                            print("Proxy invalid or blocked")
                            break
                    gleam.Destroy()

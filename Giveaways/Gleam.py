from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType

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

    def Setup(self, proxy):
        chrome_options = webdriver.ChromeOptions()
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.http_proxy = proxy
        prox.ssl_proxy = proxy

        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)
        #chrome_options.add_argument('--proxy-server=' + proxy)
        if str(socket.gethostbyname(socket.gethostname())) == "192.168.8.182":
            self.driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
        else:
            self.driver = webdriver.Chrome("../Files/chromedriver.exe", options=chrome_options, desired_capabilities=capabilities)

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

    def Start(self, url, firstname, lastname, email):
        try:
            info = [firstname, lastname, email]
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
                        time.sleep(1)
                        self.driver.find_elements(By.XPATH, "//button[@ng-click='setContestant()']")[0].click()
                        for i in range(60):
                            element = self.driver.find_element_by_class_name("tally")
                            if "Deine Teilnahme am Gewinnspiel ist bestätigt" in element.get_attribute("uib-tooltip"):
                                return True
                            time.sleep(0.1)
                        return False
                time.sleep(0.5)
        except Exception as ex:
            print(str(ex))
            return False


if __name__ == "__main__":
    proxyBroker = ProxyBroker()
    proxyGenerator = SpyScraper()
    proxies = proxyGenerator.GetProxies(500)
    #proxies = proxyBroker.GetProxies(50)
    #print(*proxies, sep="\n")
    infoGenerator = InfoGenerator()
    manager = GivawayManager()
    giveaways = manager.GetOpenGiveaways()
    gleam = Gleam()

    if len(giveaways) > 0:
        for giveaway in giveaways:
            url = giveaway[1]
            id = giveaway[0]
            counter = 1
            #for proxy in ["103.78.23.26:8080 "]:
            for ip, port, latency, uptime in proxies:
                proxy = ":".join([ip, port])
                print("Using Proxy " + proxy)
                gleam.Setup(proxy)
                gleam.driver.get("https://httpbin.org/ip")
                time.sleep(100)
                for i in range(20):
                    email = infoGenerator.GenerateEmail("testmail")
                    firstname = infoGenerator.GenerateFirstname()
                    lastname = infoGenerator.GenerateLastname()
                    if gleam.Start(url, firstname, lastname, email):
                        print(f"{counter}, Entered {email}")
                        counter = counter + 1
                        manager.EnterEmailAccount(email, id)
                    else:
                        break
                gleam.Destroy()

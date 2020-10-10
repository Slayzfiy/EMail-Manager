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

    def Setup(self):
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--proxy-server=' + proxy)
        #chrome_options.add_argument("--headless")

        if "127" in str(socket.gethostbyname(socket.gethostname())):
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome("../../Files/chromedriver.exe", options=chrome_options)

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
            time.sleep(1)

            entryMethods = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'entry-method')]")
            if len(entryMethods) > 0:
                entryMethods[0].click()

            for j in range(10):
                fieldsets = self.driver.find_elements(By.XPATH, "//fieldset[@class='inputs']")
                for fieldset in fieldsets:
                    if fieldset.is_displayed():
                        container = fieldset.find_element(By.XPATH, ".//div[contains(@class, 'contestant-form-group')]")
                        elements = container.find_elements(By.XPATH, "./div")
                        for element in elements:
                            self.HandleElement(element, info)

                        for element in self.driver.find_elements(By.XPATH, "//button[@ng-click='setContestant()']"):
                            try:
                                element.click()
                            except:
                                pass
                        time.sleep(1)
                        window = self.driver.current_window_handle
                        self.driver.find_elements(By.XPATH, "//a[@href='https://www.facebook.com/Tenda-Technology-Germany-1622263621177848']")[0].click()
                        time.sleep(2)
                        self.driver.switch_to.window(window)
                        self.driver.execute_script('document.getElementsByClassName("text user-links entry-method-title ng-scope ng-binding")[1].click()')
                        time.sleep(2)
                        self.driver.find_elements(By.XPATH, "//a[@href='https://twitter.com/Tenda_Germany']")[0].click()
                        time.sleep(2)
                        self.driver.switch_to.window(window)
                        time.sleep(2)
                        return True
                time.sleep(0.5)
            return False
        except:
            return False


if __name__ == "__main__":
    infoGenerator = InfoGenerator()
    manager = GivawayManager()
    id = manager.GetOpenGiveaways()[0][0]
    gleam = Gleam()
    url = "https://gleam.io/xZKhQ/gewinnspiel-tenda-nova-mw12"
    gleam.Setup()
    counter = 0
    for i in range(21):
        info = [infoGenerator.GenerateFirstname(), infoGenerator.GenerateLastname(), infoGenerator.GenerateEmail("testmail")]
        if gleam.Start(url, info):
            counter += 1
            print(f"{counter}. Entered {info[2]}")
            manager.EnterEmailAccount(info[2], id)
    gleam.Destroy()

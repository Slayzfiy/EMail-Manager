from Giveaways.GiveawayManager import GivawayManager as gm

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
import time


class Gleam:
    def __init__(self):
        self.driver = webdriver.Chrome("../Files/chromedriver.exe")

    def Start(self, email, url):
        try:
            self.Clear()
            self.driver.get(url)
            time.sleep(3)
            firstname = str(email).split(".")[0]
            lastname = str(email).split(".")[1].split("@")[0][:-5]
            self.driver.find_elements_by_name("firstname")[2].send_keys(firstname)
            self.driver.find_elements_by_name("lastname")[2].send_keys(lastname)
            self.driver.find_elements_by_name("email")[2].send_keys(email)
            self.driver.find_elements_by_name("land")[1].send_keys("Ö")
            self.driver.execute_script('document.getElementsByName("hiermit_akzeptiere_ich_die_teilnahmebedingungen")[1].click()')
            time.sleep(1)
            self.driver.execute_script('document.getElementsByClassName("btn btn-primary ng-scope")[1].click()')
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, '//a[contains(text(), "Jetzt hier klicken!")]'))).click()
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[0])
            for i in range(60):
                element = self.driver.find_element_by_class_name("tally")
                if "Deine Teilnahme am Gewinnspiel ist bestätigt" in element.get_attribute("uib-tooltip"):
                    return True
                time.sleep(0.1)
            return False
        except Exception as ex:
            print("Crashed because of " + str(ex))
            return False

    def Clear(self):
        self.driver.delete_all_cookies()
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])


if __name__ == "__main__":
    gm = gm()
    gleam = Gleam()

    giveaway = gm.GetOpenGiveaways()[0]
    url = giveaway[1]
    id = giveaway[0]
    counter = 1
    for tempEmail in gm.GetMissingEmails(1):
        email = tempEmail[0]
        if gleam.Start(email, url):
            print("Successfull (%s)" % counter)
            gm.EnterEmailAccount(email, id)
            counter += 1

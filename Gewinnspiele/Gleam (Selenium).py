from Emails.SQLManager import MySQLManager as sql
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time


class Gleam:
    def __init__(self, url, email):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.url = url
        self.email = email

    def Start(self):
        self.driver.get(self.url)
        time.sleep(5)
        firstname = str(self.email).split(".")[0]
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.NAME, "firstname"))).send_keys(firstname)


if __name__ == "__main__":
    gleam = Gleam("https://gleam.io/1QcZ2/gewinnspiel-samsung-galaxy-book-ion", "email.sakdhjaksdj@gmail.com")
    gleam.Start()
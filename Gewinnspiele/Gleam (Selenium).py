from Emails.SQLManager import MySQLManager as sql
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class Gleam:
    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver.exe")

    def Start(self):
        pass


if __name__ == "__main__":
    gleam = Gleam()
    gleam.Start()
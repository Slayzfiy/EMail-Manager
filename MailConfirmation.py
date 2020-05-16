from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

import time


def GETFROMSQLSERVER():
    return 'hallo'


class MailConfirmation:
    def __init__(self):
        self.first_name = GETFROMSQLSERVER()
        self.last_name = GETFROMSQLSERVER()
        self.password = GETFROMSQLSERVER()
        self.musician = GETFROMSQLSERVER()
        self.username = GETFROMSQLSERVER()
        self.number = GETFROMSQLSERVER()
        self.driver = webdriver.Chrome

    def Login(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://passport.yandex.com/registration")
        firstnameField = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//input[@id='firstname']")))
        firstnameField.send_keys(self.first_name)
        self.driver.find_element_by_id("lastname").send_keys(self.last_name)
        self.driver.find_element_by_id("login").send_keys(self.username)
        self.driver.find_element_by_id("password").send_keys(self.password)
        self.driver.find_element_by_id("password_confirm").send_keys(self.password)

        self.driver.find_element_by_xpath("//span[@class='toggle-link link_has-no-phone']").click()
        self.driver.find_element_by_id("hint_answer").send_keys(self.musician)

        image_url = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//img[class='captcha__image']")))

        print(image.get_attribute("src"))


if __name__ == "__main__":
    a = MailConfirmation()
    a.Login()

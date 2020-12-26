from Tools.InfoGenerator import InfoGenerator
from Tools.ProxyGenerator import Webshare

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import random
import time
import socket




class Bot:
    def __init__(self):
        self.driver = None

    def setup(self, proxy):
        chrome_options = webdriver.ChromeOptions()
        ip = proxy[0]
        port = proxy[1]
        chrome_options.add_argument(f"--proxy-server=http://{ip}:{port}")
        #chrome_options.add_argument("--headless")

        if "127" in str(socket.gethostbyname(socket.gethostname())):
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome("../../Files/chromedriver.exe", options=chrome_options)

    def close(self):
        self.driver.close()

    def start(self, ig):
        tag = ig.GenerateTestmail()
        email = f"ui38k.{tag}@inbox.testmail.app"
        password = ig.GeneratePassword()
        firstname = ig.GenerateFirstname()
        lastname = ig.GenerateLastname()
        birthdate = ig.GenerateBirthdate("dmy")
        country = "Österreich"

        self.driver.delete_all_cookies()
        self.driver.get("https://www.instant-gaming.com/de/giveaway/NEWYEAR2021")

        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, "//a[contains(@class, 'ig-logged-link')]"))).click()
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.ID, "ig-register-manual"))).click()

        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "ig-email"))).send_keys(email)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "ig-pass"))).send_keys(password)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "ig-firstname"))).send_keys(firstname)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "ig-lastname"))).send_keys(lastname)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "ig-birthdate"))).send_keys(birthdate)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "ig-country"))).send_keys(country)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "ig-register-terms-input"))).click()

        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "g-recaptcha"))).click()

        time.sleep(10000)


if __name__ == "__main__":
    infoGenerator = InfoGenerator("../../Files/firstnames.json", "../../Files/lastnames.json", 6)
    webshare = Webshare()
    bot = Bot()

    counter = 0
    proxies = webshare.GetProxies()
    bot.setup(random.choice(proxies))
    for i in range(1):
        bot.start(infoGenerator)

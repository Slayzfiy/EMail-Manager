import re
import traceback
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import time
from Tools.InfoGenerator import InfoGenerator
from Tools.Fabio_SQLManager import SQLManager
from Tools.MedionNewsletterConfirmator import Query


class Medion:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()

        self.driver = webdriver.Chrome("../Files/chromedriver.exe", options=chrome_options)

    def Start(self):
        counter = 0
        while True:
            try:
                info = InfoGenerator()
                email = info.GenerateEmail('testmail')
                url = 'https://www.medion.com/de/shop/newsletter-registration-inscopenico?email=%s' % (
                    email.replace("%", "%40"))

                self.driver.delete_all_cookies()
                self.driver.get(url)

                # fields
                salutation_field = 'address.title'
                lastname_field = 'address.lastName'
                firstname_field = 'address.firstName'
                birthday_field = 'register.birthday'

                # values
                first_name = info.GenerateFirstname()
                last_name = info.GenerateLastname()
                birthday = info.GenerateBirthday()

                # fill in information
                select = Select(WebDriverWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.ID, salutation_field))))
                select.select_by_value('mr')
                WebDriverWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.ID, lastname_field))).send_keys(last_name)
                WebDriverWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.ID, firstname_field))).send_keys(first_name)
                WebDriverWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.ID, birthday_field))).send_keys(birthday)

                time.sleep(2)
                self.driver.execute_script("document.getElementById('newsletter.terms1').click();")
                time.sleep(2)
                self.driver.execute_script("document.getElementsByClassName('btn btn--primary btn--block "
                                           "js-nl-submit-btn')[0].click();")

                time.sleep(4)

                # upload to sql
                self.Upload_Data_To_SQL(email, first_name, last_name, birthday)
                print(counter, 'subscribed with:', email)
                time.sleep(2)
                counter += 1

                if counter > 30:
                    time.sleep(30)
                    confirmer = Query()
                    confirmer.Confirm()

            except Exception:
                print(traceback.format_exc())

    def Upload_Data_To_SQL(self, email, firstname, lastname, birthday):
        sql = SQLManager("web.hak-kitz.at", "fabio.kreisern", "MyDatabase056", "fabio.kreisern_")
        cmd = "INSERT INTO MedionAccountsInfos (firstname, lastname, sex, birthday, email) VALUES" \
              "('%s', '%s','Mr','%s', '%s')" % (firstname, lastname, birthday, email)
        print(cmd)
        sql.Execute_Cmd(cmd)


    def Clear(self):
        self.driver.delete_all_cookies()
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])


if __name__ == "__main__":
    bot = Medion()
    bot.Start()




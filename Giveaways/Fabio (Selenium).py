import logging
import re
import traceback

import requests

from Giveaways.GiveawayManager import GivawayManager as gm

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import time
from Tools.InfoGenerator import InfoGenerator


class Medion:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome("../Files/chromedriver.exe", options=chrome_options)

    # def Start(self, email, url):
    #     try:
    #         post_infos = {
    #             "origin": "gw_leadgen_DE_MEDION_0720_ inscopenico",
    #             "salutation": "mr",
    #             "firstname": "fasdf",
    #             "lastname": "asfsdfasdfasdf",
    #             "email": email,
    #             "birthday": "05.06.2002",
    #             "honeypot": "mr"
    #         }
    #         mail = email.replace("@", "%40")
    #         session = requests.Session()
    #         my_referer = "https://www.medion.com/de/shop/newsletter-registration-inscopenico?email=%s" % mail
    #         print(my_referer)
    #         session.headers.update({'referer': my_referer})
    #
    #         r = session.get("https://www.medion.com/de/shop/newsletter-registration-inscopenico?email=%s" % mail)
    #         header = r.headers
    #         cookie = r.cookies
    #         print("1.", header, cookie)
    #
    #         r = session.post("https://www.medion.com/de/shop/newsletter/subscribe", params=post_infos, headers=header,
    #                          cookies=cookie)
    #         cookies = r.cookies
    #         header = r.headers
    #         print("2.", header, cookie)
    #
    #         x = requests.get('https://www.medion.com/de/shop/newsletter-success', cookies=cookies, headers=header)
    #
    #         print(x.cookies)
    #
    #         print("joined with: ", email)
    #
    #     except Exception as ex:
    #         print("Crashed because of " + str(ex))
    #         return False

    def Start(self):
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

                for x in range(5):
                    if self.driver.current_url == 'https://www.medion.com/de/shop/newsletter-success':
                        print('subscribed with:', email)
                        break
                    else:
                        time.sleep(1)
                else:
                    print("didn't subscribe with email:", email)

            except Exception:
                print(traceback.format_exc())

    def Confirm_Newsletter(self):
        test_mail_url = 'https://api.testmail.app/api/json?apikey=25ad9e51-ce4d-4bcb-b15f-b8dbd2779ca0&namespace=ui38k&pretty=true'
        confirmation_reg = 'https:\\/\\/link.newsletter.medion.com\\/u\\/nrd.*?(?= target)'

        emails_html = requests.get(test_mail_url).text

        codes = re.findall(confirmation_reg, emails_html)
        print(any(codes.count(x) > 1 for x in codes))
        print(codes)


def Clear(self):
    self.driver.delete_all_cookies()
    if len(self.driver.window_handles) > 1:
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


if __name__ == "__main__":
    bot = Medion()
    # bot.Start()
    bot.Confirm_Newsletter()

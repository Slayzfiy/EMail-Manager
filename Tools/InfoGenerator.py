import random
import string
import json
import os


class InfoGenerator:
    def __init__(self):
        self.firstnames = json.load(open(os.path.dirname(os.path.realpath(__file__)).strip("Tools") + "/Files/firstnames.json", "r"))
        self.lastnames = json.load(open(os.path.dirname(os.path.realpath(__file__)).strip("Tools") + "/Files/lastnames.json", "r"))
        self.chars = string.digits + string.ascii_letters
        self.randomNumberLength = 5

        self.emailFormat = '{0}.{1}{2}{3}'
        self.testmailFormat = 'ui38k.{0}@inbox.testmail.app'
        self.birthdayFormat = '{}.{}.{}'
        self.passwordLength = 15

    def GenerateFirstname(self):
        return str(self.firstnames[random.randint(0, len(self.firstnames) - 1)]).capitalize()

    def GenerateLastname(self):
        return str(self.lastnames[random.randint(0, len(self.lastnames) - 1)]).capitalize()

    def GenerateRandomNumber(self):
        return "".join(random.choice(string.digits) for i in range(self.randomNumberLength))

    def GenerateCombination(self, length):
        return "".join(random.choice(self.chars) for i in range(length - 1)) + random.choice(string.digits)

    def GeneratePassword(self):
        return "".join(random.choice(self.chars) for i in range(self.passwordLength - 1)) + random.choice(string.digits)

    def GenerateBirthday(self):
        date = random.randint(1, 28)
        month = random.randint(1, 12)
        year = random.randint(1960, 2000)
        return self.birthdayFormat.format(date, month, year)

    def GenerateEmail(self, type):
        firstname = self.GenerateFirstname()
        lastname = self.GenerateLastname()
        number = self.GenerateRandomNumber()
        if type == "dhosting":
            return str(self.emailFormat.format(firstname, lastname, number, "@dhosting.com"))
        elif type == "testmail":
            return str(self.testmailFormat.format(self.GenerateCombination(10)))
        elif type == "protonmail":
            return str(self.emailFormat.format(firstname, lastname, number, ""))

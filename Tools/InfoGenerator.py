import random
import string
import json


class InfoGenerator:
    def __init__(self):
        self.firstnames = json.load(open("../Files/firstnames.json", "r"))
        self.lastnames = json.load(open("../Files/lastnames.json", "r"))
        self.chars = string.digits + string.ascii_letters
        self.randomNumberLength = 5

        self.format = "firstname.lastnamenumberemail"
        self.passwordLength = 15

    def SetCustomEmailFormat(self, format):
        self.format = format

    def GenerateFirstname(self):
        return str(self.firstnames[random.randint(0, len(self.firstnames) - 1)])

    def GenerateLastname(self):
        return str(self.lastnames[random.randint(0, len(self.lastnames) - 1)]).capitalize()

    def GenerateRandomNumber(self):
        return "".join(random.choice(string.digits) for i in range(self.randomNumberLength))

    def GenerateEmail(self, type):
        if type == "dhosting":
            firstname = self.GenerateFirstname()
            lastname = self.GenerateFirstname()
            email = self.format.replace("firstname", str(firstname)).replace("lastname", str(lastname))
            email = email.replace("number", self.GenerateRandomNumber())
            email = email.replace("email", "@dhosting.com")
            return str(email)
        elif type == "testmail":
            combination = self.GenerateCombination(10)
            format = "ui38k.combination@inbox.testmail.app"
            return format.replace("combination", combination)

    def GenerateCombination(self, length):
        return "".join(random.choice(self.chars) for i in range(length - 1)) + random.choice(string.digits)

    def GeneratePassword(self):
        return "".join(random.choice(self.chars) for i in range(self.passwordLength - 1)) + random.choice(string.digits)

    def GenerateBirthday(self):
        date = random.randint(1, 28)
        month = random.randint(1, 12)
        year = random.randint(1960, 2000)
        return '{}.{}.{}'.format(date, month, year)

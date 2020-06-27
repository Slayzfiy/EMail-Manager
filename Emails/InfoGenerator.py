import random
import string
import json


class InfoGenerator:
    def __init__(self, firstnamesPath, lastnamesPath, randomNumberLength):
        self.firstnames = json.load(open(firstnamesPath, "r"))
        self.lastnames = json.load(open(lastnamesPath, "r"))
        self.chars = string.digits + string.ascii_letters
        self.randomNumberLength = randomNumberLength

        self.format = "firstname.lastnamenumberemail"
        self.passwordLength = 15

    def SetCustomEmailFormat(self, format):
        self.format = format

    def GenerateFirstname(self):
        return self.firstnames[random.randint(0, len(self.firstnames) - 1)]

    def GenerateLastname(self):
        return self.lastnames[random.randint(0, len(self.lastnames) - 1)]

    def GenerateRandomNumber(self):
        return "".join(random.choice(string.digits) for i in range(self.randomNumberLength))

    def GenerateEmail(self, emailSuffix):
        firstname = self.GenerateFirstname()
        lastname = self.GenerateFirstname()
        email = self.format.replace("firstname", str(firstname)).replace("lastname", str(lastname))
        email = email.replace("number", self.GenerateRandomNumber())
        email = email.replace("email", emailSuffix)
        return email

    def GeneratePassword(self):
        return "".join(random.choice(self.chars) for i in range(self.passwordLength - 1)) + "0"
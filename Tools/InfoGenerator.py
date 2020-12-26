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
        return str(self.firstnames[random.randint(0, len(self.firstnames) - 1)]).capitalize()

    def GenerateLastname(self):
        return str(self.lastnames[random.randint(0, len(self.lastnames) - 1)]).capitalize()

    def GenerateUsername(self):
        chars = string.ascii_letters + string.digits
        username = "".join([random.choice(chars) for i in range(15)])
        return username

    def GenerateRandomNumber(self):
        return "".join(random.choice(string.digits) for i in range(self.randomNumberLength))

    def GenerateEmail(self, emailSuffix):
        firstname = self.GenerateFirstname()
        lastname = self.GenerateFirstname()
        email = self.format.replace("firstname", str(firstname)).replace("lastname", str(lastname))
        email = email.replace("number", self.GenerateRandomNumber())
        email = email.replace("email", emailSuffix)
        return str(email)

    def GeneratePassword(self):
        return "".join(random.choice(self.chars) for i in range(self.passwordLength - 1)) + random.choice(string.digits)

    @staticmethod
    def GenerateTestmail():
        return "".join([random.choice(string.ascii_letters) for i in range(10)])

    @staticmethod
    def GenerateBirthdate(format):
        day = random.randint(1, 27)
        month = random.randint(1, 12)
        year = random.randint(1980, 2000)
        return str(format).replace("d", str(day)).replace("m", str(month)).replace("y", str(year))
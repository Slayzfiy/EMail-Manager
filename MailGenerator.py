import MySQLdb
import json
import random


def Get_first_name():
    return json.load(open("firstnames.json", "r"))[random.randint(0, 299)]


def Get_last_name():
    return str(json.load(open("lastnames.json", "r"))[random.randint(0, 299)]).capitalize()


def Get_number():
    return str(random.randint(100, 10000))


def Get_Email(firstName, lastName, number, prefix):
    return "%s.%s%s%s" % (firstName, lastName, number, prefix)


def Get_musician():
    return "%s %s" % (getFirstname(), getLastname())


def Get_password():
    import string
    return "".join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for i in
                   range(random.randint(10, 15)))


class MailGenerator(object):
    def __init__(self):
        self.first_name = Get_first_name()
        self.last_name = Get_last_name()
        self.password = Get_password()
        self.musician = Get_musician()
        self.username = Get_Email()
        self.number = Get_number()

    def uploadAccount(self):
        global cursor
        cursor.execute(
            "insert into 1swp_email_accounts_yandex (Firstname, Lastname, Number, Email, Musician, Password) "
            "values('%s', '%s', '%s', '%s', '%s', '%s')" % (
                self.first_name, self.last_name, self.number, self.username, self.musician, self.password))

    def start(self):
        db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
        cursor = db.cursor()
        prefix = "@yandex.com"

        for i in range(10):
            firstname = getFirstname()
            lastname = getLastname()
            number = getNumber()
            email = getEmail(firstname, lastname, number, prefix)
            musician = getMusician()
            password = getPassword()
            print("Creating %s" % email)
            uploadAccount(firstname, lastname, number, email, musician, password)

        db.commit()

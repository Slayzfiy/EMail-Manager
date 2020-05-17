import MySQLdb
import json
import random
import datetime
import string


def uploadAccount(cursor, firstname, lastname, number, email, musician, password):
    cursor.execute(
        "insert into 1swp_email_account_templates (Firstname, Lastname, Number, Email, Musician, Password) values('%s', '%s', '%s', '%s', '%s', '%s')" % (
        firstname, lastname, number, email, musician, password))


db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
cursor = db.cursor()
prefix = "@yandex.com"
numberTemplates = 16583

firstnames = json.load(open("firstnames.json", "r"))
lastnames = json.load(open("lastnames.json", "r"))


timestamp = datetime.datetime.now()
for i in range(1, numberTemplates + 1):

    firstname = firstnames[random.randint(0, 299)]
    lastname = lastnames[random.randint(0, 299)].capitalize()
    number = str(random.randint(100, 10000))
    email = "%s.%s%s%s" % (firstname, lastname, number, prefix)
    musician = "%s %s" % (firstnames[random.randint(0, 299)], lastnames[random.randint(0, 299)].capitalize())
    password = "".join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for i in range(random.randint(10, 15)))
    uploadAccount(cursor, firstname, lastname, number, email, musician, password)

    if i % 100 == 0:
        print("Created %s Accounts" % i)

db.commit()
print("Created %s templates (took %s)" % (numberTemplates, (datetime.datetime.now() - timestamp)))

import MySQLdb
import imaplib
import email as emaila
import time


class Mail_manager:
    def __init__(self):
        self.db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
        self.cursor = self.db.cursor()

    def Get_Emails(self):
        self.cursor.execute(
            "select Email from 1swp_eg_accounts where Status = 'Waiting'")
        data = []
        for line in self.cursor.fetchall():
            data.append(line[0])
        self.db.commit()
        return data

    def Save_Code(self, email, code, codetype):
        self.cursor.execute("update 1swp_eg_accounts set %s = '%s' where Email = '%s'" % (codetype, code, email))
        self.db.commit()

    def  Get_Email_Password(self, email):
        self.cursor.execute(
            "select Password from 1swp_email_dhosting where Email = '%s'" % email)
        return self.cursor.fetchone()[0]

    def Get_Code(self, email, password, codetype):
        code = ""
        # filters to filter the mails
        sender_filter = "Epic Games <help@acct.epicgames.com>"
        if codetype == 'verification':
            subject_filter = 'Epic Games - Email Verification'

        elif codetype == '2fa':
            subject_filter = 'Dein Zwei-Faktor-Anmeldecode'

        mail = imaplib.IMAP4_SSL("imap.dhosting.com")
        mail.login(email, password)
        mail.select("inbox")

        for ID in mail.search(None, 'ALL')[1][0].split():
            data = mail.fetch(ID, "(RFC822)")[1]
            email_message = emaila.message_from_string(data[0][1].decode("UTF-8"))
            if (email_message['From']) == sender_filter:
                if (email_message['Subject']) == subject_filter:
                    i = 0
                    for part in email_message.walk():
                        i += 1
                        if i == 2 and codetype == "verification":
                            body = str(part.get_payload(decode=True)).replace("\\r", "").replace("\\n", "")
                            temp = body.split('<div style="font-family: arial,helvetica,sans-serif; mso-line-height-rule: exactly; color:#313131; text-align: center; font-size: 50px; letter-spacing: 20px; line-height: 120px;">')[1]
                            code = temp[:6]
                        elif i == 2 and codetype == "2fa":
                            body = str(part.get_payload(decode=True)).replace("\\r", "").replace("\\n", "")
                            temp = body.split('<div style="font-family: arial,helvetica,sans-serif; mso-line-height-rule: exactly; color:#313131; text-align: center; font-size: 40px; letter-spacing: 15px; line-height: 100px;">')[1]
                            code = temp[:6]
        return code


if __name__ == "__main__":
    i = Mail_manager()
    while True:
        for email in i.Get_Emails():
            print("Checking Email %s" % email)
            pw = i.Get_Email_Password(email)
            print(email + ", " + pw)

            code1 = i.Get_Code(email, pw, 'verification')
            if code1 != "":
                i.Save_Code(email, code1, "Code1")
                print("Saved Code1 %s for %s" % (code1, email))

            code2 = i.Get_Code(email, pw, '2fa')
            if code2 != "":
                i.Save_Code(email, code2, "Code2")
                print("Saved Code2 %s for %s" % (code2, email))

        time.sleep(5)
        print("Waiting...")


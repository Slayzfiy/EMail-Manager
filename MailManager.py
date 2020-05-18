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
        return data

    def Save_Code(self, email, code, codetype):
        self.cursor.execute("update 1swp_eg_accounts set %s = '%s', Status = 'Nothing' where Email = '%s'" % (codetype, code, email))
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
            subject_filter = 'Your two-factor sign in code'

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
                        if i == 2:
                            body = str(part.get_payload(decode=True)).replace("\\r", "").replace("\\n", "")
                            temp = body.split('<div style="font-family: arial,helvetica,sans-serif; mso-line-height-rule: exactly; color:#313131; text-align: center; font-size: 50px; letter-spacing: 20px; line-height: 120px;">')[1]
                            code = temp[:6]
        return code


if __name__ == "__main__":
    i = Mail_manager()
    while True:
        for email in i.Get_Emails():
            pw = i.Get_Email_Password(email)
            print(email + ", " + pw)
            code = i.Get_Code(email, pw, 'verification')
            if code != "":
                i.Save_Code(email, code, "Code1")
                print("Saved Code %s for %s" % (code, email))
        time.sleep(5)
        print("Waiting...")


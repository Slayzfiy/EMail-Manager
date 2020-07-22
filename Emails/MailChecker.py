import imaplib
import email as e
from email.header import decode_header
from Emails.SQLManager import MySQLManager as sql


class MailChecker:
    def __init__(self):
        self.sqlManager = sql("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")

    def GetMails(self, email, password):
        mails = []
        mail = imaplib.IMAP4_SSL("imap.dhosting.com")

        try:
            mail.login(email, password)
        except:
            print("Invalid Credentials")
            return []

        mail.select("inbox")
        for ID in mail.search(None, 'ALL')[1][0].split():
            data = mail.fetch(ID, "(RFC822)")[1]
            email_message = e.message_from_string(data[0][1].decode("UTF-8"))
            i = 0
            for part in email_message.walk():
                i += 1
                if i == 2:
                    body = str(part.get_payload(decode=True)).replace("\\r", "").replace("\\n", "")
                    mails.append(body)
        return mails


if __name__ == "__main__":
    checker = MailChecker()
    counter = 1
    for email in checker.sqlManager.getData("dhosting_giveaway_entries", "Email"):
        email = email[0]
        password = checker.sqlManager.getData("dhosting_email_accounts", "Password", f"where Email ='{email}'")[0][0]
        print(f"({counter}) Checking {email} using Password {password}")
        mails = checker.GetMails(email, password)
        if not mails == []:
            print("\n" + "\n".join(mails) + "\n")
        counter += 1


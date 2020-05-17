import MySQLdb
import imaplib
import email as emaila
from bs4 import BeautifulSoup


class Mail_manager:
    def __init__(self):
        pass

    def Fetch_Mail_Infos(self):
        db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
        cursor = db.cursor()
        cursor.execute(
            "select Email, Password from 1swp_email_accounts order by Rand() limit 1")
        data = cursor.fetchone()
        return data

    def Fetch_Mails(self, email, password, codetype):

        # filters to filter the mails
        sender_filter = "help@acct.epicgames.com"
        if codetype == 'verification':
            subject_filter = 'Epic Games - Email Verification'
        elif codetype == '2fa':
            subject_filter = 'Your two-factor sign in code'

        mail = imaplib.IMAP4_SSL("imap.yandex.com")
        mail.login(email, password)
        mail.select("inbox")

        for ID in mail.search(None, 'ALL')[1][0].split():
            data = mail.fetch(ID, "(RFC822)")[1]
            email_message = emaila.message_from_string(data[0][1].decode("UTF-8"))
            for payload in email_message.get_payload():
                print(('From:\t', email_message['From']))
                if ('From:\t', email_message['From']) == sender_filter:
                    if ('Subject:', email_message['Subject']) == subject_filter:
                        for part in email_message.walk():
                            body = part.get_payload(decode=True)
                            sourcecode = BeautifulSoup(str(body), "html.parser")


if __name__ == "__main__":
    i = Mail_manager()
    #email, pw = i.Fetch_Mail_Infos()
    #print(email, pw)
    email, pw = 'Aaliyah.Cochran9639@yandex.com', 'oKrFFQ1vasvUsES'
    i.Fetch_Mails(email, pw, '2fa')

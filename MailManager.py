import MySQLdb
import imaplib
import email as emaila
from bs4 import BeautifulSoup
import re


class Mail_manager:
    def __init__(self):
        pass

    def Fetch_Mail_Infos(self):
        db = MySQLdb.connect("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
        cursor = db.cursor()
        cursor.execute(
            "select Email, Password from 1swp_email_dhosting order by Rand() limit 1")
        data = cursor.fetchone()
        return data

    def Fetch_Mails(self, email, password, codetype):

        # filters to filter the mails
        sender_filter = "Epic Games <help@acct.epicgames.com>"
        if codetype == 'verification':
            subject_filter = 'Epic Games - Email Verification'
            code_filter_indicator = '\r\n</div>\r\n'

        elif codetype == '2fa':
            subject_filter = 'Your two-factor sign in code'

        mail = imaplib.IMAP4_SSL("imap.dhosting.com")
        mail.login(email, password)
        mail.select("inbox")

        for ID in mail.search(None, 'ALL')[1][0].split():
            data = mail.fetch(ID, "(RFC822)")[1]
            email_message = emaila.message_from_string(data[0][1].decode("UTF-8"))
            for payload in email_message.get_payload():
                if (email_message['From']) == sender_filter:
                    if (email_message['Subject']) == subject_filter:
                        for part in email_message.walk():
                            body = part.get_payload(decode=True)
                            sourcecode = BeautifulSoup(str(body), "html.parser")
                            #print(sourcecode)
                            #code = re.search("^n[0-9]{6}", str(sourcecode))



                            ele = sourcecode.find_all('div', attrs={'style': 'font-family:arial,helvetica,sans-serif; color: '
                                                                    '#313131;text-align: center;font-size: '
                                                                    '50px;letter-spacing: 20px;line-height: 120px;'})
git
                            for x in ele:
                                print(x.text)


                            #print(sourcecode[index:index+5])


if __name__ == "__main__":
    i = Mail_manager()
    # email, pw = i.Fetch_Mail_Infos()
    # print(email, pw)
    email, pw = 'JourneyOwen1377@dhosting.email', 'aLIgyFA3u6M'
    i.Fetch_Mails(email, pw, 'verification')

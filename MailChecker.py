import MySQLdb
import imaplib
import email as emaila
import subprocess


def Get_Code(email, password):
    code = ""
    # filters to filter the mails
    sender_filter = "Epic Games <help@epicgames.com>"
    subject_filter = 'Your Security Code'

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
                        temp = body.split(
                            '<div style="font-family: arial,helvetica,sans-serif; mso-line-height-rule: exactly; '
                            'color:#313131; text-align: center; font-size: 50px; letter-spacing: 20px; line-height: '
                            '120px;">')[1]
                        code = temp[:6]
    return code


def copy2clip(txt):
    return subprocess.run('clip', universal_newlines=True, input=txt)


mail = input('email: ')
password = input('password: ')
code = Get_Code(mail, password)
print('\nCode: %s copied to clipboard!' % code)
copy2clip(code)

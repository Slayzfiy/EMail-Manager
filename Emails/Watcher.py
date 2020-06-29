from Emails.SQLManager import MySQLManager as sql
from Emails.MailGenerator import MailGenerator as generator
import time


class Watcher:
    def __init__(self):
        self.sqlManager = sql("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
        self.mailGenerator = generator()

    def HostTooOld(self):
        return not self.sqlManager.dataExists("dhosting_host_accounts", "WHERE TIMESTAMPADD(Hour, 1, Created) > now() order By Created desc limit 1")

    def RefreshHost(self):
        self.mailGenerator.DeleteEmailAccounts()

        self.mailGenerator.CreateHostAccount()
        time.sleep(10)
        hostAccount = self.mailGenerator.GetLatestHostAccount()
        dsid = self.mailGenerator.GetdsID(hostAccount)
        for account in self.sqlManager.getData("dhosting_email_accounts", "Email, Password"):
            self.mailGenerator.SendCreateRequest(account[0], account[1], dsid, hostAccount)
            time.sleep(5)

    def Start(self):
        while True:
            self.__init__()
            try:
                while True:
                    emailAccounts = len(self.sqlManager.getData("dhosting_email_accounts", "Email, Password"))
                    print(f"Currently got: {emailAccounts} Email Accounts")
                    if self.HostTooOld():
                        print("Host is too old, creating a new one!")
                        self.RefreshHost()
                    elif emailAccounts < 1000:
                        hostName = self.mailGenerator.GetLatestHostAccount()
                        hostPassword = self.sqlManager.getData("dhosting_host_accounts", "(Password)", f"where Name ='{hostName}'")
                        dsid = self.mailGenerator.GetdsID(hostName, hostPassword)
                        for i in range(1000 - emailAccounts):
                            self.mailGenerator.CreateEmailAccount(hostName, dsid)
                            time.sleep(5)
                            print("Created Account.")
                    else:
                        print("Nothing to do.")
                    time.sleep(60)
            except Exception as e:
                print(e)
                print("Restarting")


if __name__ == "__main__":
    watcher = Watcher()
    watcher.Start()

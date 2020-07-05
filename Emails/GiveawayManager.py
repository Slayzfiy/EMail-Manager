from Emails.SQLManager import MySQLManager as sql


class GivawayManager:
    def __init__(self):
        self.sqlManager = sql("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")

    def GetMissingEmails(self, giveawayID):
        return self.sqlManager.getData("dhosting_email_accounts", "Email", f"WHERE Email not in (select Email from dhosting_giveaway_entries where GiveawayID = {giveawayID})")

    def GetOpenGiveaways(self):
        return self.sqlManager.getData("dhosting_giveaways", "ID, URL", "where DrawDate > Now()")

    def EnterEmailAccount(self, email, giveawayID):
        self.sqlManager.insertData("dhosting_giveaway_entries", "(Email, GiveawayID)", [email, giveawayID])

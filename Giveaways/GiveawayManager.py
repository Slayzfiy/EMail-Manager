from Tools.SQLManager import MySQLManager as sql


class GivawayManager:
    def __init__(self):
        self.sqlManager = sql("web.hak-kitz.at", "m.beihammer", "MyDatabase047", "m.beihammer")
        self.prefix = "py_"
        self.giveawayTable = self.prefix + "Giveaways"
        self.giveawayEntriesTable = self.prefix + "Giveaway_Entries"

    def GetOpenGiveaways(self):
        return self.sqlManager.getData(self.giveawayTable, "ID, URL", "where DrawDate > Now()")

    def EnterEmailAccount(self, email, giveawayID):
        self.sqlManager.insertData(self.giveawayEntriesTable, "(Email, GiveawayID)", [email, giveawayID])

    def RegisterGiveaway(self, product, url, date):
        self.sqlManager.insertData(self.giveawayTable, "(Product, URL, DrawDate)", [product, url, date])

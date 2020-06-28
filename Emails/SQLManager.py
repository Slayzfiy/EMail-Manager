import MySQLdb


class MySQLManager:
    def __init__(self, server, database, password, username):
        self.connection = MySQLdb.connect(server, database, password, username)
        self.cursor = self.connection.cursor()

    def insertData(self, table, datafields, data):
        dataValues = "'"
        for item in data:
            dataValues += str(item) + "', '"
        dataValues = dataValues[:-3]
        self.cursor.execute(f"insert into {table} {datafields} values(%s)" % dataValues)
        self.connection.commit()

    def updateData(self, table, datafield, value, condition):
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"update {table} set {datafield} = '{value}' {condition}")
        self.connection.commit()

    def getData(self, table, datafields, condition=""):
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select {datafields} from {table} {condition}")

        if "limit 1" in condition:
            return self.cursor.fetchone()
        return self.cursor.fetchall()

    def dataExists(self, table, condition):
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"select * from {table} {condition}")
        return len(self.cursor.fetchall()) > 0

    def deleteData(self, table, condition):
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"delete from {table} {condition}")
        self.connection.commit()

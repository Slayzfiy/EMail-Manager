import MySQLdb


class SQLManager:
    def __init__(self, server, username, password, database):
        self.server = server
        self.username = username
        self.database = database
        self.password = password
        self.connection = None
        self.cursor = None

    def Open_Connection(self):
        self.connection = MySQLdb.connect(self.server, self.username, self.password, self.database)
        self.cursor = self.connection.cursor()

    def Close_Connection(self):
        self.cursor.close()
        self.connection.close()

    def Execute_Cmd(self, statement):
        self.Open_Connection()
        self.cursor.execute(statement)
        self.connection.commit()
        self.Close_Connection()

    def Retrieve_Data(self, columnsToSelect, table):
        self.Open_Connection()
        if type(columnsToSelect) is list:
            selectedColumns = ','.join(columnsToSelect)
        self.cursor.execute("SELECT %s FROM %s" % (columnsToSelect, table))
        self.Close_Connection()





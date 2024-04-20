from PyQt6.QtSql import QSqlQuery, QSqlDatabase


class DataBase():
    def __init__(self):
        super().__init__()
        self.listOfTableNames = ["categories", "tasks"]


    def createConnection(self):
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName("DB_tasklist.sqlite")
        if not self.con.open():
            QMessageBox.critical(None, "Пример QTableView — ошибка!",
                "Ошибка базы данных: %s" % self.con.lastError().databaseText(),
            )
            return False
        return True


    def initTables(self):
        self.con.open()
        self.query = QSqlQuery()
        self.query.exec(
            f"""
                CREATE TABLE IF NOT EXISTS {self.listOfTableNames[0]} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255) NOT NULL
                )
            """
        )
        self.query.exec(
            f"""
                CREATE TABLE IF NOT EXISTS {self.listOfTableNames[1]} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255) NOT NULL,
                    description VARCHAR(255) NOT NULL,
                    active VARCHAR(3) NOT NULL,
                    category_id INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            """
        )
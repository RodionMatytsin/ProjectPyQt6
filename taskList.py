from PyQt6.QtSql import QSqlQuery, QSqlDatabase
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QListWidgetItem
from PyQt6.QtWidgets import QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt


class TaskList(QWidget):
    def __init__(self):
        super().__init__()
        self.listOfTableNames = ["categories", "tasks"]
        self.listStatusActive = ["Активная", "Выполненная"]
        self.initUI()
        self.setStructure()
        self.createConnection()
        self.initTables()
        self.get_task()
        self.get_categories()


    def initUI(self):
        self.resize(500, 650)
        self.setWindowTitle("Список задач")
        self.vbox = QVBoxLayout()
        self.hbox1, self.hbox2, self.hbox3, self.hbox4, self.hbox5, \
        self.hbox6, self.hbox7, self.hbox8, self.hbox9 = [QHBoxLayout() for i in range(9)]

        self.label_task = QLabel("Список задач:", self)
        self.label_taskname = QLabel("Название задачи:", self)
        self.task_dicrpt = QLabel("Описание задачи:", self)
        self.label_category = QLabel("Название категории:", self)
        self.label_active = QLabel("Активная задача:", self)
        self.label_category_id = QLabel("Категория ID:", self)
        self.label_list_of_categories = QLabel("Список категорий:", self)

        self.task_list, self.task_list_of_categories = [QListWidget() for i in range(2)]

        self.btn_all_tasks = QPushButton("Все задачи", self)
        self.btn_all_tasks.clicked.connect(self.get_task)
        self.btn_active_tasks = QPushButton("Активные задачи", self)
        self.btn_active_tasks.clicked.connect(self.get_active_task)
        self.btn_complete_tasks = QPushButton("Выполненные задачи", self)
        self.btn_complete_tasks.clicked.connect(self.get_complete_task)

        self.btn_add_tasks = QPushButton("Добавить задачу", self)
        self.btn_add_tasks.clicked.connect(self.add_task)
        self.btn_change_tasks = QPushButton("Изменить задачу", self)
        self.btn_change_tasks.clicked.connect(self.change_task)
        self.btn_delete_tasks = QPushButton("Удалить задачу", self)
        self.btn_delete_tasks.clicked.connect(self.delete_task)
        self.btn_clear_tasks = QPushButton("Очистить поля", self)
        self.btn_clear_tasks.clicked.connect(self.clear_task)

        self.btn_all_categories = QPushButton("Все категории", self)
        self.btn_all_categories.clicked.connect(self.get_categories)
        self.btn_clear_categories = QPushButton("Очистить поле категории", self)
        self.btn_clear_categories.clicked.connect(self.clear_categories)
        self.btn_add_categories = QPushButton("Добавить категорию", self)
        self.btn_add_categories.clicked.connect(self.add_categories)
        self.btn_change_categories = QPushButton("Изменить категорию", self)
        self.btn_change_categories.clicked.connect(self.change_categories)
        self.btn_delete_categories = QPushButton("Удалить категорию", self)
        self.btn_delete_categories.clicked.connect(self.delete_categories)

        self.task_name_line, self.task_category_line, self.task_active_line, \
        self.category_id_line = [QLineEdit() for i in range(4)]
        self.task_dicrpt_text = QTextEdit()

        self.task_list.itemClicked.connect(self.onListItemClicked)
        self.task_list_of_categories.itemClicked.connect(self.onListOfCategoriesItemClicked)


    def setStructure(self):
        self.vbox.addWidget(self.label_task)
        self.vbox.addWidget(self.task_list)

        self.hbox1.addWidget(self.btn_all_tasks)
        self.hbox1.addWidget(self.btn_active_tasks)
        self.hbox1.addWidget(self.btn_complete_tasks)
        self.vbox.addLayout(self.hbox1)

        self.hbox2.addWidget(self.label_taskname)
        self.hbox2.addWidget(self.task_name_line)
        self.vbox.addLayout(self.hbox2)

        self.hbox3.addWidget(self.label_active)
        self.hbox3.addWidget(self.task_active_line)
        self.vbox.addLayout(self.hbox3)

        self.hbox4.addWidget(self.task_dicrpt)
        self.hbox4.addWidget(self.task_dicrpt_text)
        self.vbox.addLayout(self.hbox4)

        self.hbox5.addWidget(self.label_category_id)
        self.hbox5.addWidget(self.category_id_line)
        self.vbox.addLayout(self.hbox5)

        self.hbox6.addWidget(self.btn_add_tasks)
        self.hbox6.addWidget(self.btn_change_tasks)
        self.hbox6.addWidget(self.btn_delete_tasks)
        self.hbox6.addWidget(self.btn_clear_tasks)
        self.vbox.addLayout(self.hbox6)

        self.hbox7.addWidget(self.label_category)
        self.hbox7.addWidget(self.task_category_line)
        self.vbox.addLayout(self.hbox7)

        self.vbox.addWidget(self.label_list_of_categories)
        self.vbox.addWidget(self.task_list_of_categories)

        self.hbox8.addWidget(self.btn_all_categories)
        self.hbox8.addWidget(self.btn_clear_categories)
        self.vbox.addLayout(self.hbox8)

        self.hbox9.addWidget(self.btn_add_categories)
        self.hbox9.addWidget(self.btn_change_categories)
        self.hbox9.addWidget(self.btn_delete_categories)
        self.vbox.addLayout(self.hbox9)

        self.setLayout(self.vbox)


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


    def onListItemClicked(self):
        selectedTask = self.task_list.currentItem()
        if selectedTask is not None:
            taskData = self.tasks[self.task_list.row(selectedTask)]
            self.task_name_line.setText(str(taskData[1]))
            self.task_dicrpt_text.setText(str(taskData[2]))
            self.task_active_line.setText(str(taskData[3]))
            self.category_id_line.setText(str(taskData[4]))
            if str(taskData[3]) == "0":
                self.task_active_line.setText(self.listStatusActive[0])
            elif str(taskData[3]) == "1":
                self.task_active_line.setText(self.listStatusActive[1])
        else:
            self.clear_task()


    def onListOfCategoriesItemClicked(self):
        selectedCategories = self.task_list_of_categories.currentItem()
        if selectedCategories is not None:
            categoriesData = self.categories[self.task_list_of_categories.row(selectedCategories)]
            self.category_id_line.setText(str(categoriesData[0]))
            self.task_category_line.setText(str(categoriesData[1]))
        else:
            self.clear_categories()


    def clear_task(self):
        self.task_name_line.clear()
        self.task_active_line.clear()
        self.task_dicrpt_text.clear()
        self.category_id_line.clear()


    def clear_categories(self):
        self.task_category_line.clear()
        self.category_id_line.clear()


    def get_task(self, status : str = ""):
        if status == "Активные задачи":
            query = f"""
                        SELECT *
                        FROM {self.listOfTableNames[1]}
                        WHERE active = 0
                    """
        elif status == "Выполненные задачи":
            query = f"""
                        SELECT *
                        FROM {self.listOfTableNames[1]}
                        WHERE active = 1
                    """
        else:
            query = f"""
                        SELECT *
                        FROM {self.listOfTableNames[1]}
                        LEFT JOIN {self.listOfTableNames[0]} ON category_id = {self.listOfTableNames[0]}.id;
                    """
        self.query.exec(query)
        self.tasks = []
        while self.query.next():
            self.tasks.append([self.query.value(i) for i in range(self.query.record().count())])
        print(self.tasks)
        self.task_list.clear()
        for task in self.tasks:
            self.task_list.addItem(QListWidgetItem(task[1]))


    def get_active_task(self):
        self.get_task(str("Активные задачи"))


    def get_complete_task(self):
        self.get_task(str("Выполненные задачи"))


    def add_task(self):
        task_name = self.task_name_line.text()
        task_description = self.task_dicrpt_text.toPlainText()
        active_task = self.task_active_line.text()
        category_id = self.category_id_line.text()
        if not task_name or not category_id:
            QMessageBox.critical(self, "Ошибка", "Текстовые поля 'Название задачи' или 'Категория ID' должны быть заполнены!")
            return
        if active_task not in self.listStatusActive:
            QMessageBox.critical(self, "Ошибка",
                f"Значение задачи должно быть 'Активная' или 'Выполненная'. Получено: {active_task}"
            )
            return
        active_task_bool = self.listStatusActive.index(active_task)
        self.query.exec(
            f"""
                INSERT INTO {self.listOfTableNames[1]} (name, description, active, category_id)
                VALUES ('{task_name}', '{task_description}', {active_task_bool}, '{category_id}');
            """
        )
        print(self.query.lastError().text() if not self.query.isActive() else "Запрос активен")
        self.get_task()


    def change_task(self):
        current_task = self.task_list.currentItem()
        new_task_name = self.task_name_line.text()
        new_active_task = self.task_active_line.text()
        new_task_description = self.task_dicrpt_text.toPlainText()
        category_id = self.category_id_line.text()
        if not new_task_name or not category_id:
            QMessageBox.critical(self, "Ошибка", "Текстовые поля 'Название задачи' или 'Категория ID' должны быть заполнены!")
            return
        if new_active_task not in self.listStatusActive:
            QMessageBox.critical(self, "Ошибка",
                f"Значение задачи должно быть 'Активная' или 'Выполненная'. Получено: {new_active_task}"
            )
            return
        new_active_task_bool = self.listStatusActive.index(new_active_task)
        self.query.exec(
            f"""
                SELECT id FROM {self.listOfTableNames[1]}
                WHERE name = '{current_task.text()}'
                LIMIT 1
            """
        )
        if self.query.first():
            self.query.exec(
                f"""
                    UPDATE {self.listOfTableNames[1]}
                    SET name = '{new_task_name}', description = '{new_task_description}', 
                    active = '{new_active_task_bool}', category_id = '{category_id}'
                    WHERE id = '{self.query.value(0)}'
                """
            )
        else:
            QMessageBox.information(self, "Информация", "Задача не найдена.")
        print(self.query.lastError().text() if not self.query.isActive() else "Запрос активен")
        current_task.setText(new_task_name)
        self.task_dicrpt_text.setText(new_task_description)
        print(f"Обновленная задача: {new_task_name} - {new_task_description} - {new_active_task_bool}")
        self.get_task()


    def delete_task(self):
        try:
            current_task = self.task_list.currentItem()
            self.query.exec(
                f"""
                    SELECT id FROM {self.listOfTableNames[1]}
                    WHERE name = '{current_task.text()}'
                    LIMIT 1
                """
            )
            if self.query.first():
                self.query.exec(
                    f"""
                        DELETE FROM {self.listOfTableNames[1]}
                        WHERE id = '{self.query.value(0)}'
                    """
                )
            else:
                QMessageBox.information(self, "Информация", "Задача не найдена.")
            print(self.query.lastError().text() if not self.query.isActive() else "Запрос активен")
            self.task_list.takeItem(self.task_list.row(current_task))
            self.get_task()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"При удалении задачи произошла ошибка: {e}")
            print(f"Ошибка: {e}")


    def get_categories(self):
        self.query.exec(
            f"""
                SELECT *
                FROM {self.listOfTableNames[0]}
            """
        )
        self.categories = []
        while self.query.next():
            self.categories.append([self.query.value(i) for i in range(self.query.record().count())])
        print(self.categories)
        self.task_list_of_categories.clear()
        for categ in self.categories:
            self.task_list_of_categories.addItem(QListWidgetItem(categ[1]))


    def add_categories(self):
        name_categories = self.task_category_line.text()
        if not name_categories:
            QMessageBox.critical(self, "Ошибка", "Текстовое поле 'Название категории' должно быть заполнено!")
            return
        self.query.exec(
            f"""
                INSERT INTO {self.listOfTableNames[0]} (name)
                VALUES ('{name_categories}');
            """
        )
        print(self.query.lastError().text() if not self.query.isActive() else "Запрос активен")
        self.get_categories()


    def change_categories(self):
        current_categories = self.task_list_of_categories.currentItem()
        new_name_categories = self.task_category_line.text()
        if not new_name_categories:
            QMessageBox.critical(self, "Ошибка", "Текстовое поле 'Название категории' должно быть выбрано или заполнено!")
            return
        self.query.exec(
            f"""
                SELECT id FROM {self.listOfTableNames[0]}
                WHERE name = '{current_categories.text()}'
                LIMIT 1
            """
        )
        if self.query.first():
            self.query.exec(
                f"""
                    UPDATE {self.listOfTableNames[0]}
                    SET name = '{new_name_categories}'
                    WHERE id = '{self.query.value(0)}'
                """
            )
        else:
            QMessageBox.information(self, "Информация", "Категория не найдена.")
        print(self.query.lastError().text() if not self.query.isActive() else "Запрос активен")
        current_categories.setText(new_name_categories)
        print(f"Обновленная категория: {new_name_categories}")
        self.get_categories()


    def delete_categories(self):
        try:
            current_categories = self.task_list_of_categories.currentItem()
            self.query.exec(
                f"""
                    SELECT id FROM {self.listOfTableNames[0]}
                    WHERE name = '{current_categories.text()}'
                    LIMIT 1
                """
            )
            if self.query.first():
                self.query.exec(
                    f"""
                        DELETE FROM {self.listOfTableNames[0]}
                        WHERE id = '{self.query.value(0)}'
                    """
                )
            else:
                QMessageBox.information(self, "Информация", "Категория не найдена.")
            print(self.query.lastError().text() if not self.query.isActive() else "Запрос активен")
            self.task_list.takeItem(self.task_list.row(current_categories))
            self.get_categories()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"При удалении категории произошла ошибка: {e}")
            print(f"Ошибка: {e}")

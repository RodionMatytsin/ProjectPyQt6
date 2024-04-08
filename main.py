import sys
from PyQt6.QtWidgets import QApplication
from taskList import TaskList


def main():
    app = QApplication(sys.argv)
    window = TaskList()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

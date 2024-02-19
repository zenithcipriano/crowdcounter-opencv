import sys

from PyQt5.QtWidgets import QApplication

from src.window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.startLoop()
    app.exec_()


if __name__ == "__main__":
    main()

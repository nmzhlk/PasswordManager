import sqlite3
import sys

from PyQt5 import QtWidgets, QtGui
from dotenv import load_dotenv

from AuthorizationDialog import AuthorizationDialog as StarterWindow

load_dotenv()  # Токен шифрования

# База данных
con = sqlite3.connect('passwords.db')
cur = con.cursor()

if __name__ == '__main__':
    Application = QtWidgets.QApplication(sys.argv)
    Application.setWindowIcon(QtGui.QIcon('icon.png'))
    Window = QtWidgets.QDialog()
    GUI = StarterWindow()
    GUI.setupUi(Window)
    Window.show()
    sys.exit(Application.exec_())

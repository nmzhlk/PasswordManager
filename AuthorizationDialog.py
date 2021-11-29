import os
import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets
from cryptography.fernet import Fernet  # Для шифрования пароля
from dotenv import load_dotenv

from AccountCreationDialog import AccountCreationDialog as creator
from MainWindow import MainWindow as main

load_dotenv()  # Токен шифрования

# База данных
con = sqlite3.connect('passwords.db')
cur = con.cursor()


class AuthorizationDialog(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 350)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.create_button = QtWidgets.QPushButton(self.centralwidget)
        self.create_button.setGeometry(QtCore.QRect(25, 305, 350, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.create_button.setFont(font)
        self.create_button.setObjectName("create_button")
        self.login_button = QtWidgets.QPushButton(self.centralwidget)
        self.login_button.setGeometry(QtCore.QRect(25, 255, 350, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.login_button.setFont(font)
        self.login_button.setObjectName("login_button")
        self.guide_label = QtWidgets.QLabel(self.centralwidget)
        self.guide_label.setGeometry(QtCore.QRect(115, 50, 200, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.guide_label.setFont(font)
        self.guide_label.setObjectName("guide_label")
        self.password_label = QtWidgets.QLabel(self.centralwidget)
        self.password_label.setGeometry(QtCore.QRect(25, 180, 350, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        self.username_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.username_edit.setGeometry(QtCore.QRect(25, 130, 350, 30))
        self.username_edit.setObjectName("username_edit")
        self.username_label = QtWidgets.QLabel(self.centralwidget)
        self.username_label.setGeometry(QtCore.QRect(25, 100, 350, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.password_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.password_edit.setGeometry(QtCore.QRect(25, 210, 350, 30))
        self.password_edit.setObjectName("password_edit")
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(80, 10, 250, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.title_label.setObjectName("title_label")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.create_button.clicked.connect(self.creation_window)
        self.login_button.clicked.connect(self.login)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Менеджер паролей: Авторизация"))
        self.create_button.setText(_translate("MainWindow", "Создать аккаунт"))
        self.login_button.setText(_translate("MainWindow", "Войти"))
        self.guide_label.setText(_translate("MainWindow", "Войдите в аккаунт"))
        self.password_label.setText(_translate("MainWindow", "Пароль"))
        self.username_label.setText(_translate("MainWindow", "Имя пользователя"))
        self.title_label.setText(_translate("MainWindow", "Менеджер паролей"))

    def creation_window(self):
        dialog = QtWidgets.QDialog()
        ui = creator()
        ui.setupUi(dialog)
        dialog.exec()

    def login(self):
        if not self.username_edit.text() or not self.password_edit.text():
            self.username_edit.setText('Введите данные для входа')
            self.password_edit.setText('Введите данные для входа')
        if not self.username_checker():
            self.username_edit.setText('Неверное имя пользователя')
        elif not self.password_checker():
            self.password_edit.setText('Неверный пароль')
        else:
            cur.execute("INSERT INTO Logs VALUES (?)", (self.username_edit.text(),))
            con.commit()
            window = QtWidgets.QDialog()
            ui = main()
            ui.setupUi(window)
            window.exec()

    def username_checker(self):
        cur.execute("SELECT username FROM Accounts")
        usernames = cur.fetchall()
        username = self.username_edit.text()
        for i in range(len(usernames)):
            if username == usernames[i][0]:
                return True
        return False

    def password_checker(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        cur.execute("SELECT password FROM Accounts WHERE username == ?", (username,))
        correct_password = cur.fetchone()

        # Расшифровка пароля
        key = os.getenv('KEY')
        fernet = Fernet(key)
        decrypted_password = fernet.decrypt(correct_password[0]).decode()
        if decrypted_password == password:
            return True
        return False

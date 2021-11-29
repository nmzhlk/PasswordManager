import os
import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets
from cryptography.fernet import Fernet  # Для шифрования пароля
from dotenv import load_dotenv

load_dotenv()  # Токен шифрования

# База данных
con = sqlite3.connect('passwords.db')
cur = con.cursor()


class AccountCreationDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 350)
        self.guide_label_2 = QtWidgets.QLabel(Dialog)
        self.guide_label_2.setGeometry(QtCore.QRect(120, 50, 200, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.guide_label_2.setFont(font)
        self.guide_label_2.setObjectName("guide_label_2")
        self.title_label_2 = QtWidgets.QLabel(Dialog)
        self.title_label_2.setGeometry(QtCore.QRect(80, 10, 250, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.title_label_2.setFont(font)
        self.title_label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.title_label_2.setObjectName("title_label_2")
        self.username_label = QtWidgets.QLabel(Dialog)
        self.username_label.setGeometry(QtCore.QRect(25, 100, 350, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.password_label = QtWidgets.QLabel(Dialog)
        self.password_label.setGeometry(QtCore.QRect(25, 185, 350, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        self.create_button = QtWidgets.QPushButton(Dialog)
        self.create_button.setGeometry(QtCore.QRect(25, 280, 350, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.create_button.setFont(font)
        self.create_button.setObjectName("pushButton")
        self.password_edit = QtWidgets.QLineEdit(Dialog)
        self.password_edit.setGeometry(QtCore.QRect(25, 215, 350, 30))
        self.password_edit.setObjectName("password_edit")
        self.username_edit = QtWidgets.QLineEdit(Dialog)
        self.username_edit.setGeometry(QtCore.QRect(25, 130, 350, 30))
        self.username_edit.setObjectName("username_edit")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.create_button.clicked.connect(self.save_info)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Менеджер паролей: Создание аккаунта"))
        self.guide_label_2.setText(_translate("Dialog", "Создайте аккаунт"))
        self.title_label_2.setText(_translate("Dialog", "Менеджер паролей"))
        self.username_label.setText(_translate("Dialog", "Имя пользователя"))
        self.password_label.setText(_translate("Dialog", "Пароль"))
        self.create_button.setText(_translate("Dialog", "Сохранить"))

    def username_checker(self, username):
        cur.execute("SELECT username FROM Accounts")
        usernames = cur.fetchall()
        for i in range(len(usernames)):
            if username == usernames[i][0]:
                return False
        return True

    def save_info(self):
        if not self.username_edit.text() or not self.password_edit.text():
            self.username_edit.setText('Введите данные')
            self.password_edit.setText('Введите данные')
        username = self.username_edit.text()
        if not self.username_checker(username):
            self.username_edit.setText('Имя пользователя уже существует')
        else:
            password = self.password_edit.text()

            # Шифрование пароля с использованием ключа, сохраненного в файле .env
            key = os.getenv('KEY')
            fernet = Fernet(key)
            encrypted_password = fernet.encrypt(password.encode())

            cur.execute("INSERT INTO Accounts VALUES(?, ?)", (username, encrypted_password))
            con.commit()
            self.create_button.setText('Данные добавлены. Вы можете закрыть это окно')

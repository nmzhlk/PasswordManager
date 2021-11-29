import os
import random
import sqlite3
import string

from PyQt5 import QtCore, QtGui, QtWidgets
from cryptography.fernet import Fernet  # Для шифрования пароля
from dotenv import load_dotenv

load_dotenv()  # Токен шифрования

# База данных
con = sqlite3.connect('passwords.db')
cur = con.cursor()


class DataAdditionDialog(object):
    def setupUi(self, AddDataDialog):
        AddDataDialog.setObjectName("AddDataDialog")
        AddDataDialog.resize(400, 350)
        self.title_label = QtWidgets.QLabel(AddDataDialog)
        self.title_label.setGeometry(QtCore.QRect(100, 10, 200, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.service_label = QtWidgets.QLabel(AddDataDialog)
        self.service_label.setGeometry(QtCore.QRect(25, 50, 350, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.service_label.setFont(font)
        self.service_label.setObjectName("service_label")
        self.service_edit = QtWidgets.QLineEdit(AddDataDialog)
        self.service_edit.setGeometry(QtCore.QRect(25, 80, 350, 30))
        self.service_edit.setObjectName("service_edit")
        self.username_edit = QtWidgets.QLineEdit(AddDataDialog)
        self.username_edit.setGeometry(QtCore.QRect(25, 160, 350, 30))
        self.username_edit.setObjectName("username_edit")
        self.username_label = QtWidgets.QLabel(AddDataDialog)
        self.username_label.setGeometry(QtCore.QRect(25, 130, 350, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.password_edit = QtWidgets.QLineEdit(AddDataDialog)
        self.password_edit.setGeometry(QtCore.QRect(25, 240, 350, 30))
        self.password_edit.setObjectName("password_edit")
        self.password_label = QtWidgets.QLabel(AddDataDialog)
        self.password_label.setGeometry(QtCore.QRect(25, 210, 350, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        self.secure_password_button = QtWidgets.QPushButton(AddDataDialog)
        self.secure_password_button.setGeometry(QtCore.QRect(200, 210, 175, 25))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.secure_password_button.setFont(font)
        self.secure_password_button.setObjectName("secure_password_button")
        self.save_button = QtWidgets.QPushButton(AddDataDialog)
        self.save_button.setGeometry(QtCore.QRect(25, 290, 350, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.save_button.setFont(font)
        self.save_button.setObjectName("pushButton")

        self.retranslateUi(AddDataDialog)
        QtCore.QMetaObject.connectSlotsByName(AddDataDialog)

        self.save_button.clicked.connect(self.save_data)
        self.secure_password_button.clicked.connect(self.secure_password_generator)

    def retranslateUi(self, AddDataDialog):
        _translate = QtCore.QCoreApplication.translate
        AddDataDialog.setWindowTitle(
            _translate("AddDataDialog", "Менеджер паролей: Добавление данных"))
        self.title_label.setText(_translate("AddDataDialog", "Добавление данных"))
        self.service_label.setText(_translate("AddDataDialog", "Название сервиса"))
        self.username_label.setText(_translate("AddDataDialog", "Имя пользователя"))
        self.password_label.setText(_translate("AddDataDialog", "Пароль"))
        self.secure_password_button.setText(_translate("AddDataDialog", "Создать надежный пароль"))
        self.save_button.setText(_translate("AddDataDialog", "Сохранить"))

    def secure_password_generator(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password_length = random.randint(8, 14)
        generated_password = ''.join(random.choice(characters) for x in range(password_length))
        self.password_edit.setText(generated_password)

    def current_account(self):
        cur.execute("SELECT username FROM Logs")
        accounts_list = cur.fetchall()
        logged_account = accounts_list[len(accounts_list) - 1][0]
        return logged_account

    def save_data(self):
        current_account = self.current_account()
        service_name = self.service_edit.text()
        service_username = self.username_edit.text()
        service_password = self.password_edit.text()

        if not service_name or not service_username or not service_password:
            self.service_edit.setText('Введите данные')
            self.username_edit.setText('Введите данные')
            self.password_edit.setText('Введите данные')
        else:
            # Шифрование пароля
            key = os.getenv('KEY')
            fernet = Fernet(key)
            encrypted_password = fernet.encrypt(service_password.encode())

            cur.execute("INSERT INTO Data VALUES (?, ?, ?, ?)",
                        (service_name, service_username, encrypted_password, current_account))
            con.commit()
            self.save_button.setText('Данные сохранены. Вы можете закрыть это окно')
            self.service_edit.setText('')
            self.username_edit.setText('')
            self.password_edit.setText('')

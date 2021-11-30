import os
import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets
from cryptography.fernet import Fernet  # Для шифрования пароля
from dotenv import load_dotenv

from DataAdditionDialog import DataAdditionDialog as data_dialog

load_dotenv()  # Токен шифрования

# База данных
con = sqlite3.connect('passwords.db')
cur = con.cursor()


class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 600)
        self.password_label = QtWidgets.QLabel(MainWindow)
        self.password_label.setGeometry(QtCore.QRect(20, 450, 600, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        self.username_line = QtWidgets.QLineEdit(MainWindow)
        self.username_line.setGeometry(QtCore.QRect(20, 380, 600, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.username_line.setFont(font)
        self.username_line.setObjectName("username_line")
        self.username_label = QtWidgets.QLabel(MainWindow)
        self.username_label.setGeometry(QtCore.QRect(20, 350, 600, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.services_guide = QtWidgets.QLabel(MainWindow)
        self.services_guide.setGeometry(QtCore.QRect(20, 305, 600, 15))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.services_guide.setFont(font)
        self.services_guide.setObjectName("services_guide")
        self.services_label = QtWidgets.QLabel(MainWindow)
        self.services_label.setGeometry(QtCore.QRect(20, 80, 600, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.services_label.setFont(font)
        self.services_label.setObjectName("services_label")
        self.title_label = QtWidgets.QLabel(MainWindow)
        self.title_label.setGeometry(QtCore.QRect(150, 10, 350, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.title_label.setObjectName("title_label")
        self.services_widget = QtWidgets.QListWidget(MainWindow)
        self.services_widget.setGeometry(QtCore.QRect(20, 120, 600, 170))
        self.services_widget.setObjectName("services_widget")
        self.password_line = QtWidgets.QLineEdit(MainWindow)
        self.password_line.setGeometry(QtCore.QRect(20, 480, 600, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.password_line.setFont(font)
        self.password_line.setObjectName("password_line")
        self.add_data_button = QtWidgets.QPushButton(MainWindow)
        self.add_data_button.setGeometry(QtCore.QRect(480, 545, 140, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.add_data_button.setFont(font)
        self.add_data_button.setObjectName("add_data_button")
        self.update_data_button = QtWidgets.QPushButton(MainWindow)
        self.update_data_button.setGeometry(QtCore.QRect(440, 300, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.update_data_button.setFont(font)
        self.update_data_button.setObjectName("update_data_button")
        self.edit_data_button = QtWidgets.QPushButton(MainWindow)
        self.edit_data_button.setGeometry(QtCore.QRect(20, 545, 140, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.edit_data_button.setFont(font)
        self.edit_data_button.setObjectName("edit_data_button")

        self.add_data_button.clicked.connect(self.data_dialog)
        self.services_widget.itemDoubleClicked.connect(self.show_data)
        self.update_data_button.clicked.connect(self.services_widget_data)
        self.edit_data_button.clicked.connect(self.data_edit)
        self.services_widget_data()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Менеджер паролей"))
        self.password_label.setText(_translate("MainWindow", "Пароль"))
        self.username_label.setText(_translate("MainWindow", "Имя пользователя"))
        self.services_guide.setText(
            _translate("MainWindow", "Выберите сервис, чтобы просмотреть данные для входа"))
        self.services_label.setText(_translate("MainWindow", "Сервисы с сохранёнными данными"))
        self.title_label.setText(_translate("MainWindow", "Менеджер паролей"))
        self.add_data_button.setText(_translate("MainWindow", "Добавить данные"))
        self.update_data_button.setText(_translate("MainWindow", "Обновить данные"))
        self.edit_data_button.setText(_translate("MainWindow", "Изменить данные"))

    def data_dialog(self):
        dialog = QtWidgets.QDialog()
        ui = data_dialog()
        ui.setupUi(dialog)
        dialog.exec()

    def current_account(self):
        cur.execute("SELECT username FROM Logs")
        accounts_list = cur.fetchall()
        self.logged_account = accounts_list[len(accounts_list) - 1][0]
        return self.logged_account

    def services_widget_data(self):
        self.services_widget.clear()
        current_account = self.current_account()

        cur.execute("SELECT service_name FROM Data WHERE username == ?", (current_account,))
        shown_services = list()
        while True:
            data = cur.fetchone()
            if not data:
                break
            shown_services.append(data[0])

        self.services_widget.addItems(shown_services)

    def show_data(self, item):
        self.chosen_service = item.text()
        current_account = self.current_account()
        cur.execute(
            "SELECT service_username, service_password FROM Data "
            "WHERE username = ? AND service_name = ?",
            (current_account, self.chosen_service))
        data = cur.fetchone()

        key = os.getenv('KEY')
        fernet = Fernet(key)
        decrypted_password = fernet.decrypt(data[1]).decode()
        self.username_line.setText(data[0])
        self.password_line.setText(decrypted_password)

    def data_edit(self):
        service_password = self.password_line.text()
        service_username = self.username_line.text()
        key = os.getenv('KEY')
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(service_password.encode())
        cur.execute(
            "UPDATE Data SET service_username = ?, service_password = ? "
            "WHERE service_name = ? AND username = ?",
            (service_username, encrypted_password, self.chosen_service, self.logged_account))
        con.commit()
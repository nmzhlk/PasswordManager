import sqlite3

# Если необходимо создать таблицы в базе данных, используйте данный кусочек кода

con = sqlite3.connect('passwords.db')
cur = con.cursor()

cur.execute("""CREATE TABLE Accounts (username TEXT, password TEXT)""")
cur.execute("""CREATE TABLE Logs (username TEXT)""")
cur.execute(
    """CREATE TABLE Data (service_name TEXT, service_username TEXT, 
    service_password TEXT, username TEXT)""")

#  module_14_1

import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)""")

for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
                   (f"User{i}", f"example{i}@gmail.com", f"{i * 10}", "1000"))

cursor.execute("SELECT COUNT(*) FROM Users")
number_records = cursor.fetchall()
number_records = number_records[0][0]

for i in range(1, number_records + 1):
    if i % 2 == 1:
        cursor.execute("UPDATE users SET balance = 500 WHERE id = ?", (f"{i}",))

for i in range(1, number_records + 1):
    if i % 3 == 1:
        cursor.execute("DELETE FROM users WHERE id = ?", (f"{i}",))
connection.commit()

cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60")
users = cursor.fetchall()
for user in users:
    username, email, age, balance = user
    print(f"Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}")

connection.close()

#  crud_functions

import sqlite3

DATABASE_NAME = "telegram_145.db"

def initiate_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT NOT NULL,
price INTEGER NOT NULL
)""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER NOT NULL,
balance INTEGER NOT NULL
    )""")
    connection.commit()
    connection.close()

def add_user(username, email, age):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
                   f"({username}, {email}, {age}, 1000)")
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(username) FROM Users WHERE username = '{username}'")
    username_exists = cursor.fetchone()
    connection.close()
    return username_exists

def get_all_products():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.close()
    return products

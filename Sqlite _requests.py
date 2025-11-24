#ТХ ЗАДАНИЕ ДЛЯ СЕБЯ
#Таблица "Computer" содержит такие поля, как id, email пользователя и id программы, которое он должен взять из таблицы "PO".
#Таблица "PO-price" содержит такие поля, как id, стоимость и тоже id программы, которое он так же берёт из таблицы "PO".
#С помощью этих манипуляций мы исключаем повторение ненужного текста, потому что записываем место названия программ id, которое берём из другой таблицы.
#Нужно составить er-диаграмму, а в коде обязательно использовать внешние и внутренние ключи, чтобы все можно было вывести в виде одной таблицы через join запрос, т.е
#Первая колонка: id компьютера
#Вторая колонка: email пользователя
#Третья колонка: Название ПО
#Чётвертая колонка: Стоимость ПО

import sqlite3
connection = sqlite3.connect("KitovTop.db")
cursor = connection.cursor()

#PO
cursor.execute('''
CREATE TABLE IF NOT EXISTS PO (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Proga TEXT NOT NULL
)
''')

#Computer
cursor.execute('''
CREATE TABLE IF NOT EXISTS Computer (
    id_pc INTEGER PRIMARY KEY AUTOINCREMENT,
    Email TEXT NOT NULL,
    id_proga INTEGER,
    FOREIGN KEY(id_proga) REFERENCES PO(id)
)
''')

#PO_price
cursor.execute('''
CREATE TABLE IF NOT EXISTS PO_price (
    id_price INTEGER PRIMARY KEY AUTOINCREMENT,
    id_proga INTEGER,
    price TEXT NOT NULL,
    FOREIGN KEY(id_proga) REFERENCES PO(id)
)
''')

cursor.execute("DELETE FROM PO")
cursor.execute("DELETE FROM Computer")
cursor.execute("DELETE FROM PO_price")

#Для PO
cursor.execute('''INSERT INTO PO (Proga)
VALUES ('PyCharm')''')
cursor.execute('''INSERT INTO PO (Proga) 
VALUES ('Visual Studio')''')
cursor.execute('''INSERT INTO PO (Proga) 
VALUES ('JetBrains Package')''')

#Для Computer (id_proga соответствует id из PO)
cursor.execute('''
INSERT INTO Computer (Email, id_proga) 
VALUES ('gadakoifrazu-3290@yopmail.com', 2)
''')
cursor.execute('''
INSERT INTO Computer (Email, id_proga) 
VALUES ('jojeuneyecau-4122@yopmail.com', 1)
''')
cursor.execute('''
INSERT INTO Computer (Email, id_proga) 
VALUES ('mebitrudimma-3668@yopmail.com', 3)
''')

#Для PO_price
cursor.execute('''
INSERT INTO PO_price (id_proga, price) 
VALUES (1, '50$')
''')
cursor.execute('''
INSERT INTO PO_price (id_proga, price) 
VALUES (2, '80$')
''')
cursor.execute('''
INSERT INTO PO_price (id_proga, price) 
VALUES (3, '45$')
''')


cursor.execute('''
SELECT Computer.id_pc, Computer.Email, PO.Proga, PO_price.price FROM Computer JOIN PO ON Computer.id_proga = PO.id JOIN PO_price ON PO.id = PO_price.id_proga
''')

printf = cursor.fetchall()
for i in printf:
    print(i)
connection.commit()
connection.close()
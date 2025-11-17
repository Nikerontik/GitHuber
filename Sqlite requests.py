# # Добавляем нового пользователя
# cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', ('Mixa play', 'mixaplay@example.com', 28))

# # Обновляем возраст пользователя "newuser"
# cursor.execute('UPDATE Users SET age = ? WHERE username = ?', (29, 'Mixa play'))

# # Удаляем пользователя "newuser"
# cursor.execute('DELETE FROM Users WHERE username = ?', ('newuser',))

# # Создание индекса для столбца email
# cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users (email)')

# # Фильтруем группы по среднему возрасту больше 30
# cursor.execute('SELECT id FROM test GROUP BY id HAVING AVG(id) = ?', (4,)) #group by - группировка данных по определенным столбцам
# mid = cursor.fetchall()


import sqlite3 #Библиотека для работы с бд

# Устанавливаем соединение с бд
connection = sqlite3.connect("KitovTop.db")
cursor = connection.cursor()

#Таблица "Компьютеры"
cursor.execute('''
CREATE TABLE IF NOT EXISTS Computer (
id_pc INTEGER PRIMARY KEY AUTOINCREMENT,
Email TEXT NOT NULL,
id_proga INTEGER,
FOREIGN KEY(id_proga) REFERENCES PO(id)
)
''')


cursor.execute('''
INSERT INTO Computer (Email, id_proga) 
VALUES('gadakoifrazu-3290@yopmail.com', '2');''')

cursor.execute('''
INSERT INTO Computer (Email, id_proga) 
VALUES('jojeuneyecau-4122@yopmail.com', '1');''')

cursor.execute('''
INSERT INTO Computer (Email, id_proga) 
VALUES('mebitrudimma-3668@yopmail.com', '3');''')



#Таблица "ПО"
cursor.execute('''
CREATE TABLE IF NOT EXISTS PO (
id INTEGER PRIMARY KEY AUTOINCREMENT,
id_package INTEGER,
Proga TEXT NOT NULL,
FOREIGN KEY(id_package) REFERENCES Computer(id_pc)
)
''')

cursor.execute('''
INSERT INTO PO (Proga)
VALUES('PyCharm');''')

cursor.execute('''
INSERT INTO PO (Proga) 
VALUES('Visual Studio');''')

cursor.execute('''
INSERT INTO PO (Proga) 
VALUES('JetBrains Package');''')

#Выводим все виде одной таблицы

cursor.execute('SELECT Computer.id_pc,Computer.Email,PO.Proga FROM Computer JOIN PO ON Computer.id_proga = PO.ID') #Соединяем две колонки
Sout = cursor.fetchall() #Возвращает все строки результата запроса в виде списка

for name in Sout:
    print(name)

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()
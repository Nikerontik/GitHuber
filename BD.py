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
connection = sqlite3.connect("test.db")
cursor = connection.cursor()

# Создаем таблицу Users
#cursor.execute - Отвечает за отправку запросов
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Users (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# username TEXT NOT NULL,
# email TEXT NOT NULL,
# age INTEGER
# )
# ''')

#Подсчитываем количество записей в
cursor.execute('SELECT COUNT(*) FROM test')
total_users = cursor.fetchone()[0]

# Выбираем всех пользователей
cursor.execute('SELECT * FROM test')
users = cursor.fetchall() #Возвращает все строки результата запроса в виде списка

# Выбор опеределенного пользователя через SELECT и WHERE
cursor.execute('SELECT name, phone FROM test WHERE id = ?', (3,))
find_user = cursor.fetchall()

# Вывод результатов
for name in users:
    print(name)
print("Количество пользователей: ", total_users)
print("Пробитый пользователь:", find_user)

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()

'''
///Эта я прописывал в консоли sqlite///
CREATE TABLE test (
    id INTEGER PRIMARY KEY AUTOINCREMENT, #integer - целое число; primary key - поле id должно быть уникальным во всей таблице; AUTOINCREMENT - сама присваивает id, в mysql пишется с подчеркиванием
    name VARCHAR(50), #varchar - переменная длины символьная строка (символ)
    phone VARCHAR(50)); #varchar - переменная длины символьная строка (символ)
#SQL слова пишу большими буквами

INSERT INTO test (name, phone)
VALUES ('Nike', '89524722056');

INSERT INTO test (name, phone)
VALUES ('George', '+79200173800');

INSERT INTO test (name, phone)
VALUES ('Mixa', '+79601707518');

INSERT INTO test (name, phone)
VALUES ('Nata', '+79883140249');

INSERT INTO test (name, phone)
VALUES ('Individum', '+79200294472');
'''
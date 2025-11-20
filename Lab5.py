import sqlite3, json, csv, yaml, os # os - библиотека для работы с файловой системой

def export_simple(): #Экспорт таблицы Computer

    if not os.path.exists('out'): # Создаем папку (Если папки нету, то она создается)
        os.makedirs('out')

    conn = sqlite3.connect("KitovTop.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Computer") #Берём данные из таблицы
    data = cursor.fetchall()

    cursor.execute("PRAGMA table_info(Computer)") #Берём названия колонок
    columns = [column[1] for column in cursor.fetchall()]

    conn.close()


    # Преобразуем в словари
    data_dict = []
    for row in data:
        row_dict = {}
        for i, column in enumerate(columns):
            row_dict[column] = row[i]
        data_dict.append(row_dict)

    #JSON файл (Сохранение)
    with open('out/data.json', 'w') as f: #Открываем файл для записи JSON (Если нет - создастся)
        json.dump(data_dict, f, indent=2) #Запись данных в файл в формате JSON с отступамиы

    #CSV файл (Сохранение)
    with open('out/data.csv', 'w', newline='') as f: #Открываем файл для записи CSV (Если нет - создастся)
        writer = csv.DictWriter(f, fieldnames=columns) #объект для записи CSV с указанием названия колонок
        writer.writeheader() #Выполняем запись колонок и с помощью цикла записываем каждую строку в CSV файл
        for row in data_dict:
            writer.writerow(row)

    #XML файл (Сохранение)
    xml_content = '<?xml version="1.0"?>\n<data>\n' #Начало xml файла
    for item in data_dict: #С помощью цикла прохожу по всем элементам данных
        xml_content += '  <item>\n' #Теги для каждого элемента
        for key, value in item.items(): #Прохожу по полям
            xml_content += f'    <{key}>{value}</{key}>\n' #Тег для каждого поля
        xml_content += '  </item>\n' #Добавляю закрывающий тег для элемента
    xml_content += '</data>' #Закрываю корневой тег
    with open('out/data.xml', 'w') as f: #Открываем файл для записи XML
        f.write(xml_content) #Записываем подготовленное содержимое

    #Yaml файл
    with open('out/data.yaml', 'w') as f:  #Открываем файл для записи YAML
        yaml.dump(data_dict, f, default_flow_style=False)  #Записываем данные в YAML формате
    print("Создан файл: out/data.yaml")

    print("Успешно созданы файлы в папке 'out'")
    print(f"Количество экспортированных записей {len(data)} записей")


export_simple() #Запуск функции
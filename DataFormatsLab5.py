import sqlite3, json, csv, os

if not os.path.exists('out'):
    os.makedirs("out")

connection = sqlite3.connect("KitovTop.db")
cursor = connection.cursor()

cursor.execute('''
SELECT Computer.id_pc, Computer.Email, PO.Proga, PO_price.price FROM Computer JOIN PO ON Computer.id_proga = PO.id JOIN PO_price ON PO.id = PO_price.id_proga''')
data = cursor.fetchall()

#JSON
json_data = []
for i in data:
    json_data.append({
        'id': i[0],
        'email': i[1],
        'software': {
        'name': i[2],
        'price': i[3]
        }
    })
with open('out/data.json', 'w') as f: #открываем файл для записи JSON (если нет - создастся)
    json.dump(json_data, f, indent=2) #запись данных в файл с отступом

#CSV
with open('out/data.csv', 'w', newline='', encoding='utf-8-sig') as f: #encording нужно для указания формата UTF-8
    writer = csv.writer(f, delimiter=';') #объект, чтобы записать csv при этом с указанием названия колонок
    writer.writerow(['ID компьютера', 'Email пользователя', 'Название ПО', 'Стоимость ПО'])
    for row in data: #запись колонок через цикл
        writer.writerow([row[0], row[1], row[2], row[3]])

#XML
xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<computers>\n' #начало xml файла
for i in data: #через цикл я прохожу по всем элементам данных
    xml_content += f'''  <computer>
    <id>{i[0]}</id>
    <email>{i[1]}</email>
    <software>
        <name>{i[2]}</name>
        <price>{i[3]}</price>
    </software>
  </computer>\n'''
xml_content += '</computers>'
with open('out/data.xml', 'w') as f:
    f.write(xml_content)

#YAML
yaml_content = ''
for i in data: #записываю все колонки снова через цикл
    yaml_content += f'''- id: {i[0]}
  email: {i[1]}
  software:
    name: {i[2]}
    price: {i[3]}\n'''
with open('out/data.yaml', 'w') as f:
    f.write(yaml_content)

print("Еар! Файлики успешно были созданы (папка out)")
connection.close()
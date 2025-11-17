from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.horizontal_shard import execute_and_instances
from sqlalchemy.orm import sessionmaker, relationship

#Подключение к SQLite базе данных
engine = create_engine('sqlite:///KitovTop.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


'''Таблица с компьютерами'''
class Computer(Base):
    __tablename__ = 'Computer'

    id_pc = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100))
    id_proga = Column(Integer, ForeignKey('PO.id'))

    '''Связь один-ко-одному (или многие-к-одному)'''
    po = relationship("PO", back_populates="computer")


'''Таблица с ПО'''
class PO(Base):
    __tablename__ = 'PO'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Proga = Column(String(100))

    # Обратная связь один-ко-многим
    computer = relationship("Computer", back_populates="po")


    '''Создание всех таблиц'''
    Base.metadata.create_all(engine)


def add_data():
    #Создание PO, так как Computer ссылается на него
    po1 = PO(Proga="PyCharm")
    po2 = PO(Proga="Visual Studio")
    po3 = PO(Proga="JetBrains Package")

    session.add_all([po1, po2, po3])
    session.commit()

    '''Компьютеры, которые ссылаются на таблицу с PO'''
    computer1 = Computer(email="gadakoifrazu-3290@yopmail.com", id_proga=po1.id)
    computer2 = Computer(email="jojeuneyecau-4122@yopmail.com", id_proga=po2.id)
    computer3 = Computer(email="mebitrudimma-3668@yopmail.com", id_proga=po3.id)

    session.add_all([computer1, computer2, computer3])
    session.commit()
    print("Данные успешно добавлены!")


'''Чтение данных'''
def read_database():
    print("\nВсе компьютеры")
    all_computers = session.query(Computer).all()
    for comp in all_computers:
        print(f"ID: {comp.id_pc}, Email: {comp.email}, ID программы: {comp.id_proga}")

    print("\nВсе программы")
    all_po = session.query(PO).all()
    for po in all_po:
        print(f"ID: {po.id}, Программа: {po.Proga}")

    print("\nСвязанные данные")
    joined_data = session.query(Computer, PO).join(PO, Computer.id_proga == PO.id).all() #Запрос с JOIN для получения связанных данных
    for computer, po in joined_data:
        print(f"Компьютер {computer.email}; Программа: {po.Proga}")

'''Удаление данных(Удаляем в нужном порядке из-за внешних ключей)'''
def delete_data():
    session.query(Computer).delete()
    session.query(PO).delete()
    session.commit()
    print("Все данные удалены!")


def demonstrate_relationships():
    print("\nДемонстрация отношений")

    #Выводим таблицу компьютеров и связанное с ними ПО
    computer = session.query(Computer).first()
    if computer:
        print(f"Компьютер: {computer.email}")
        print(f"Связанная программа: {computer.po.Proga if computer.po else 'Нет программы'}")

    #Выводим таблицу с ПО и связанные с ними компьютеры
    po = session.query(PO).first()
    if po:
        print(f"\nПрограмма: {po.Proga}")
        computers_with_po = session.query(Computer).filter(Computer.id_proga == po.id).all() #Находим все компьютеры с этой программой
        for comp in computers_with_po:
            print(f"Используется на: {comp.email}")


def show_all_data():
    print("ВСЕ ДАННЫЕ ИЗ БАЗЫ\n\n")

    # Таблица PO
    print("\nТаблица PO:")
    result = session.execute(text("SELECT * FROM PO"))
    for row in result:
        print(f"ID: {row.id} Программа: {row.Proga}")

    # Таблица Computer
    print("\nТаблица Computer:")
    result = session.execute(text("SELECT * FROM Computer"))
    for row in result:
        print(f"ID: {row.id_pc} Email: {row.email} ID программы: {row.id_proga}")

# Просто добавьте эту функцию в ваш код и вызовите:
if __name__ == "__main__":
    try:
        show_all_data()  # Потом выводим всё
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        session.rollback()
    finally:
        session.close()


'''Приводим все в действие'''
if __name__ == "__main__":
    try:
        # Очищаем старые данные
        delete_data()

        # Добавляем новые данные
        add_data()

        # Читаем данные
        read_database()

        # Демонстрируем отношения
        demonstrate_relationships()

        #Вывод
        show_all_data()

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        session.rollback()
    finally:
        session.close()
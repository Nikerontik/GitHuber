from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Подключение к существующей базе
engine = create_engine('sqlite:///KitovTop.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class PO(Base): #Классы-модель для моей первой таблицы
    __tablename__ = 'PO'
    id = Column(Integer, primary_key=True)
    Proga = Column(String(100))


class Computer(Base): #Класс-модель для моей второй таблицы
    __tablename__ = 'Computer'
    id_pc = Column(Integer, primary_key=True)
    Email = Column(String(100))
    id_proga = Column(Integer, ForeignKey('PO.id'))


class PO_price(Base): #Класс-модель для моей третьей таблицы
    __tablename__ = 'PO_price'
    id_price = Column(Integer, primary_key=True)
    id_proga = Column(Integer, ForeignKey('PO.id'))
    price = Column(String(100))


#CRUD
class ComputerCRUID:
    @staticmethod
    def records(): #функция records - для получения всех записей в таблице компьютеров
        return session.query(Computer).all()

    @staticmethod
    def records_id(computer_id): #найти запись по айди в таблице с компьютерами
        return session.query(Computer).filter(Computer.id_pc == computer_id).first()

    @staticmethod
    def createrecord(email, id_proga): #добавить компьютер в бд
        computer = Computer(Email=email, id_proga=id_proga)
        session.add(computer)
        session.commit()
        return computer

    @staticmethod
    def change_email(computer_id, new_email): #поменять почту уже у существующей записи компьютера
        computer = ComputerCRUID.records_id(computer_id)
        if computer:
            computer.Email = new_email
            session.commit()
        return computer

    @staticmethod
    def deleterecord(computer_id): #удалить компьютер из бд
        computer = ComputerCRUID.records_id(computer_id)
        if computer:
            session.delete(computer)
            session.commit()


#Сервис, чтобы работать со связ-ми данными из неск-х таблиц
class ServiceTableData:
    @staticmethod
    def join_sql():
        return session.query(
            Computer.id_pc, Computer.Email, PO.Proga, PO_price.price).join(PO, Computer.id_proga == PO.id).join(
            PO_price, PO.id == PO_price.id_proga).all()

    @staticmethod
    def find_pc_po(software_name): #для нахождения компьютера с определенным по
        return session.query(Computer).join(PO).filter(PO.Proga == software_name).all()

    @staticmethod
    def find_po_price(): #для нахождения всех ПО с их ценой
        return session.query(PO, PO_price).join(PO_price, PO.id == PO_price.id_proga).all()

#краш-тест
if __name__ == "__main__":
    print("Все компьютеры ")
    computers = ComputerCRUID.records() #да-да та самая функция, которая выводит вапще всё
    for comp in computers:
        print(f"ID: {comp.id_pc}, Email: {comp.Email}, PO ID: {comp.id_proga}")

    new_comp = ComputerCRUID.createrecord("crashtest@example.com", 1) #внедряю тестовую запись
    print(f"\nДобавлен компьютер с ID: {new_comp.id_pc}")
    ComputerCRUID.change_email(new_comp.id_pc, "crashtestnew@example.com")#а затем обновляю её


    print("\nВся таблица")
    resultat = ServiceTableData.join_sql()
    print("ID | Почта | ПО | Цена")
    for id_pc, email, proga, price in resultat:
        print(f"{id_pc} | {email} | {proga} | {price}")

    print("\nВывод пк с visual studio (для теста)")
    vs_pc = ServiceTableData.find_pc_po("Visual Studio")
    for j in vs_pc:
        print(f"ID: {j.id_pc}, Email: {j.Email}")

    ComputerCRUID.deleterecord(new_comp.id_pc) #тестовый компьютер пака(удаляю)
    print(f"\nУдален компьютер с ID: {new_comp.id_pc}")

    session.close()
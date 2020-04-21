import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#путь к файлу БД
DB_PATH = 'sqlite:///sochi_athletes.sqlite3'

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)

def connect_db():
    '''Создает соединение к БД, если его нетю И возвращает объект сессии'''
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def valid_email(email):
    if "@" in email:
        email = email.split("@")
        if "." in email[1]:
            return True
        return False
def valid_birthdate(birthdate):
    res = False
    check = birthdate.split('-')
    if len(check) == 3:
        if int(check[0]) in range(1900, 2014):
            if int(check[1]) in range(1,13):
                if int(check[2]) in range(1,32):
                    res = True
    return res
def valid_gender(gender):
    return gender in ("Female", "Male")

def request_data():

    print('Введите данные пользователя')
    first_name = input('Введите имя: ')
    last_name = input('Введите фамилию: ')
    gender = input('Введите пол(Female/Male): ')
    #проверка пола
    while not valid_gender(gender):
        gender = input('Введите пол(Female/Male): ')
    email = input('Введите  email: ')

    # проверка email
    while not valid_email(email):
        print('email incorrect')
        email = input('Введите  email: ')

    birthdate = input('Введите дату рождения(гггг-мм-дд): ')

    #проверка даты рождения
    while not valid_birthdate(birthdate):
        print('Неверный формат даты')
        birthdate = input('Введите дату рождения(гггг-мм-дд): ')

    height = input('Введите рост: ')



    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )

    return user

def main():
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print('Пользователь добавлен')
if __name__ == '__main__':
    main()

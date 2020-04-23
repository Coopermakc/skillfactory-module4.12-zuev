import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


DB_PATH = 'sqlite:///sochi_athletes.sqlite3'
Base = declarative_base()

class Athelete(Base):
    __tablename__ = 'athelete'

    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

class User(Base):
        __tablename__ = 'user'

        id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
        first_name = sa.Column(sa.Text)
        last_name = sa.Column(sa.Text)
        gender = sa.Column(sa.Text)
        email = sa.Column(sa.Text)
        birthdate = sa.Column(sa.Text)
        height = sa.Column(sa.REAL)

def convert_date(date):
    return datetime.strptime(date, '%Y-%m-%d').date()

def nearest(items, thing):
    return min(items, key= lambda x: abs(x-thing))


def find(id, session):
    user = session.query(User).filter(User.id == id).first()
    if user:
        print("Найден пользователь {0} {1} день рождения {2} рост {3}".format(
                user.first_name,
                user.last_name,
                user.birthdate,
                user.height
                )
        )
        user_birthdate = convert_date(user.birthdate)

        # ищем ближайший день рождения
        atheletes = [athelete for athelete in session.query(Athelete).all()]
        nearest_date = nearest([convert_date(athelet.birthdate) for athelet in atheletes], user_birthdate)
        athlet1 = session.query(Athelete).filter(Athelete.birthdate == nearest_date).first()
        print("Ближайший день рождения у {} {}".format(athlet1.name,athlet1.birthdate))

        # ищем ближайший рост
        athlet_height = nearest([athelet.height for athelet in atheletes if athelet.height], user.height)
        athlet2 = session.query(Athelete).filter(Athelete.height == athlet_height).first()
        print("Ближайший рост у {} {}".format(athlet2.name, athlet2.height))
    else:
        print('Пользователь не найден')

def connect_db():
    '''Создает соединение к БД, если его нетю И возвращает объект сессии'''
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def main():
    session = connect_db()

    id = input('Введите id пользователя: ')
    find(id,session)

if __name__ == '__main__':
    main()

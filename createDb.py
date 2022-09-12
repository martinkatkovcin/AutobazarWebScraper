import pandas as pd
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column
import time
engine = sqlalchemy.create_engine("postgresql://postgres:postgres@localhost:5777/postgres")

Session = sessionmaker(bind = engine)
session = Session()
Base = declarative_base()

class Autobazar(Base):
    __tablename__ = 'autobazar'

    id = Column(sqlalchemy.BigInteger, primary_key=True)
    dateAdd = Column(sqlalchemy.String(255))
    link = Column(sqlalchemy.String(255))
    full_name = Column(sqlalchemy.String(255))
    mileage_km = Column(sqlalchemy.String(255))
    gear_type = Column(sqlalchemy.String(255))
    year = Column(sqlalchemy.Integer())
    fuel_type = Column(sqlalchemy.String(255))
    price = Column(sqlalchemy.String(255))

def create_database():
    Base.metadata.create_all(engine)

def fill_database(brand: str) -> None:
    car = pd.read_csv(f'cars/{brand}.csv')
    car.to_sql('autobazar', engine, if_exists = 'append', index = False)
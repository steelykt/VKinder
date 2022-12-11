import sqlalchemy as sq
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=True)
    surname = sq.Column(sq.String(length=40), nullable=True)
    age = sq.Column(sq.Integer, nullable=True)
    sex = sq.Column(sq.Integer, nullable=True)
    city = sq.Column(sq.String(length=30), nullable=True)
    city_id = sq.Column(sq.Integer, nullable=True)

    def __str__(self):
        return f'{self.id}: ({self.name}, {self.surname}, {self.age}, {self.sex}, {self.city}, {self.city_id})'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
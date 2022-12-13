import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(20), nullable=True)
    age = sq.Column(sq.Integer, nullable=True)
    sex = sq.Column(sq.Integer, nullable=True)
    city = sq.Column(sq.String(length=30), nullable=True)
    city_id = sq.Column(sq.Integer, nullable=True)

    def __str__(self):
        return f'{self.id}: ({self.name}, {self.age}, {self.sex}, {self.city}, {self.city_id})'


class Partner(Base):
    __tablename__ = 'partner'

    id = sq.Column(sq.Integer, primary_key=True)
    views = sq.Column(sq.String(10), nullable=True)
    user_id = sq.Column(sq.ForeignKey('user.id'))

    user = relationship(User, backref='partners')

    def __str__(self):
        return f'{self.id}: ({self.views}, {self.user_id})'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
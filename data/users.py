import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    """
    id              INT         ID пользователя

    name            STR         Имя пользователя

    surname         STR         Фамилия пользователя

    email           STR         Эл. почта пользователя

    phone_number    STR         Номер телефона пользователя

    hashed_password STR         Хэшированный пароль пользователя

    products        STR         Товары, которые имеет пользователь
                                 формата "id: count, id: count"

    sold_products   STR         ID товаров, которые продаёт пользователь

    card            INT         ID привязанной к пользователю карты
    """
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    phone_number = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    products = sqlalchemy.Column(sqlalchemy.String)
    sold_products = sqlalchemy.Column(sqlalchemy.String)
    card = sqlalchemy.Column(sqlalchemy.Integer)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
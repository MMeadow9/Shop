import sqlalchemy
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    """
    id              INT         ID товара

    title           STR         Название товара

    description     STR         Описание товара

    seller          INT         ID продавца

    price           INT         Цена товара

    count           INT         Кол-во имеющегося товара

    is_limited      BOOL        Ограничено ли кол-во товара
    """
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    seller = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.Integer)
    count = sqlalchemy.Column(sqlalchemy.Integer)
    is_limited = sqlalchemy.Column(sqlalchemy.Boolean)

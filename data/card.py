import sqlalchemy
from .db_session import SqlAlchemyBase


class Card(SqlAlchemyBase):
    """
    id              INT         ID карты

    number          STR         Номер карты (16 цифр)

    term            STR         Срок карты (4 цифры)

    code            STR         Код карты (3 цифры)

    cash            INT         Баланс карты

    status          STR         Статус карты (Usual, Black, Silver, Gold, Platinum),
                               позволяющий получить кэшбэк от покупок (0%, 2%, 5%, 9%, 15%)
    """
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.String)
    term = sqlalchemy.Column(sqlalchemy.String)
    code = sqlalchemy.Column(sqlalchemy.String)
    cash = sqlalchemy.Column(sqlalchemy.Integer)
    status = sqlalchemy.Column(sqlalchemy.String)

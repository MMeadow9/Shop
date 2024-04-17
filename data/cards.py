import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin



class Card(SqlAlchemyBase, SerializerMixin):
    """
    id              INT         ID карты


    number          STR         Номер карты (16 цифр)

    term            STR         Срок карты (4 цифры)

    code            STR         Код карты (3 цифры)

    cash            INT         Баланс карты

    status          STR         Статус карты (Usual, Black, Silver, Gold, Platinum),
                               позволяющий получить кэшбэк от покупок (0%, 3%, 8%, 13%, 20%)
                               а также дополнительные проценты при просмотре рекламы (0%, 0%, 5%, 15%, 30%).
                               У каждой карты своя стоимость (0₽, 250₽, 800₽, 1950₽, 3500₽)

    statuses        STR         Имеющиеся статусы у карты "1" "12345"

    """
    __tablename__ = 'cards'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.String)
    term = sqlalchemy.Column(sqlalchemy.String)
    code = sqlalchemy.Column(sqlalchemy.String)
    cash = sqlalchemy.Column(sqlalchemy.Integer)
    status = sqlalchemy.Column(sqlalchemy.String)
    statuses = sqlalchemy.Column(sqlalchemy.String)

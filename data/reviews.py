import sqlalchemy
from .db_session import SqlAlchemyBase


class Review(SqlAlchemyBase):
    """
    id      INT     ID отзыва
    comment STR     Текст отзыва
    mark    INT     Оценка продукту
    answers INT     Ответ на отзыв

    """
    __tablename__ = 'reviews'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    comment = sqlalchemy.Column(sqlalchemy.String)
    mark = sqlalchemy.Column(sqlalchemy.Integer)
    answers = sqlalchemy.Column(sqlalchemy.String)

import sqlalchemy
from .db_session import SqlAlchemyBase


class Answer(SqlAlchemyBase):
    """
    id      INT     ID ответа
    comment STR     Текст ответа
    """
    __tablename__ = 'answers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    comment = sqlalchemy.Column(sqlalchemy.String)

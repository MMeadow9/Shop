import sqlalchemy
from .db_session import SqlAlchemyBase


class Ask(SqlAlchemyBase):
    """
    id      INT     ID вопроса
    comment STR     Текст вопроса

    """
    __tablename__ = 'asks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    comment = sqlalchemy.Column(sqlalchemy.String)

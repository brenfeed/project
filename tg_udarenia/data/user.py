import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


# Класс, представляющий объект пользователя в базе данных
class User(SqlAlchemyBase, SerializerMixin):
    # Имя таблицы в базе данных
    __tablename__ = 'user'

    # Поля пользователя
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  #
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, default=None)  # Telegram ID пользователя
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=None)  # Имя пользователя
    balance = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # Баланс пользователя
    slovo = sqlalchemy.Column(sqlalchemy.String, default="")  # Слово, выбранное для ударения
    good = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # Количество правильных ответов
    bad = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # Количество неправильных ответов
    error = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # Флаг ошибки при ответе пользователя

    def __repr__(self):
        """
        Метод для представления объекта пользователя при отладке.

        :return: Строковое представление объекта.
        """
        return f'<User> {self.id} {self.name}'

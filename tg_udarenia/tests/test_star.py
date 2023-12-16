import unittest
from unittest.mock import MagicMock, patch

from data.user import User


class TestUser(unittest.TestCase):

    def setUp(self):
        # Создаем объект пользователя для тестирования
        self.user = User(tg_id=123, name="Test User", balance=10, slovo="example", good=5, bad=3, error=2)

    def test_repr(self):
        # Проверяем, что repr возвращает строку с id и именем пользователя
        expected_repr = f'<User> {self.user.id} {self.user.name}'
        self.assertEqual(repr(self.user), expected_repr, msg='Метод repr определён неверно')

    def test_default_values(self):
        # Проверяем, что все значения по умолчанию устанавливаются правильно
        default_user = User()
        self.assertEqual(default_user.tg_id, None, msg="Неверное начальное значение tg_id, должно быть None")
        self.assertEqual(default_user.name, None, msg="Неверное начальное значение name, должно быть None")
        self.assertEqual(default_user.balance, None, msg="Неверное начальное значение balance, должно быть None")
        self.assertEqual(default_user.slovo, None, msg="Неверное начальное значение slovo, должно быть None")
        self.assertEqual(default_user.good, None, msg="Неверное начальное значение good, должно быть None")
        self.assertEqual(default_user.bad, None, msg="Неверное начальное значение bad, должно быть None")
        self.assertEqual(default_user.error, None, msg="Неверное начальное значение error, должно быть None")

    def test_serialization(self):
        # Проверяем, что объект правильно сериализуется
        serialized_data = self.user.to_dict()
        expected_data = {
            'id': self.user.id,
            'tg_id': self.user.tg_id,
            'name': self.user.name,
            'balance': self.user.balance,
            'slovo': self.user.slovo,
            'good': self.user.good,
            'bad': self.user.bad,
            'error': self.user.error
        }
        self.assertEqual(serialized_data, expected_data, msg="Неверное сериализация одного или нескольких объектов")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

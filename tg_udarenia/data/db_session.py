import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

# Базовый класс для объявления моделей данных
SqlAlchemyBase = dec.declarative_base()

# Фабрика для создания сессий работы с базой данных
__factory = None


def global_init(db_file):
    """
    Инициализация подключения к базе данных.

    :param db_file: Путь к файлу базы данных.
    """
    global __factory

    # Если фабрика уже инициализирована, возвращаемся
    if __factory:
        return

    # Проверка наличия пути к файлу базы данных
    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    # Строка подключения к базе данных SQLite
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    # Создание объекта SQLAlchemy Engine для работы с базой данных
    engine = sa.create_engine(conn_str, echo=False)
    # Инициализация фабрики сессий
    __factory = orm.sessionmaker(bind=engine)

    # Импорт всех моделей данных
    from . import __all_models

    # Создание таблиц в базе данных согласно определенным моделям
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """
    Создание новой сессии работы с базой данных.

    :return: Объект сессии SQLAlchemy.
    """
    global __factory
    return __factory()


def create_session() -> Session:
    global __factory
    return __factory()

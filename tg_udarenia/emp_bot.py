import random
import telebot
from data.user import User
from telebot import types
from data import db_session

# Инициализация бота с токеном
bot = telebot.TeleBot("6747860497:AAEDN-2xGlDFj-1YZKZ6ICm6NgNXzc2n__Q")  # Токен бота


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Обработчик команды /start. Инициализация игрового процесса и приветствие пользователя.

    :param message: Объект сообщения от пользователя.
    :return: Имя пользователя.
    """
    # Отправляем стикер и приветственное сообщение с клавиатурой
    bot.send_sticker(message.from_user.id, "CAACAgIAAxkBAAJoG2V8yIHZu_8UA6E6MwYbaMXuAXmpAAIiFwAC8uFxSaWXKEXir-I2MwQ")
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)

    # Проверяем, зарегистрирован ли пользователь в базе данных, и если нет, регистрируем
    with db_session.create_session() as db_sess:
        if not db_sess.query(User).filter(User.tg_id == message.from_user.id).first():
            user = User(name=message.from_user.first_name, tg_id=message.from_user.id)
            db_sess.add(user)
            db_sess.commit()

    # Возвращаем имя пользователя
    return user.name


# Клавиатура для пользовательского ввода
keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard1.row("Начать❤️", 'Счёт🧩', "Статистика📊")
keyboard1.row("Топ🏅", 'Сброс⚠️')


# Функция для вывода топ-10 пользователей по счёту
def top(message):
    with db_session.create_session() as db_sess:
        # Получение данных о пользователях из базы данных
        user_data = []
        for user in db_sess.query(User).all():
            user_data.append([user.balance, user.name, user.tg_id])

        # Сортировка пользователей по счёту в убывающем порядке
        user_data.sort(reverse=True)

        # Формирование строки с информацией о топ-10 пользователей
        top_message = ""
        for i in range(min(10, len(user_data))):
            top_message += f"{i + 1}) {user_data[i][1]}\nСчёт: 🧩{user_data[i][0]}\n"

        # Отправка сообщения с топ-10
        bot.send_message(message.chat.id, top_message, reply_markup=keyboard1)


# Функция для инициализации игрового процесса
def game(id, call=False):
    with db_session.create_session() as db_sess:
        user = db_sess.query(User).filter(User.tg_id == id).first()

        # Если у пользователя нет ошибки, выбираем случайное слово из файла
        if user.error == 0:
            slovo = random.randint(1, 318)
            f = open("q.txt", "r", encoding="utf-8").read().split("\n")
            user.slovo = f[slovo - 1]
            db_sess.commit()

        # Создание клавиатуры с инлайн-кнопками для выбора ударения
        markup = types.InlineKeyboardMarkup()
        word = user.slovo
        for i in range(len(word)):
            if word[i].lower() in ["у", "е", "ы", "а", "о", "э", "я", "и", "ю", "ё"]:
                s = word[:i].lower() + word[i].upper() + word[i + 1:].lower()
                item = types.InlineKeyboardButton(s, callback_data=s)
                markup.add(item)

        # Отправка сообщения с инструкцией для игрока
        if not call:
            bot.send_message(id, "Поставь ударение🙉🙉🙉", reply_markup=markup)
        else:
            # Редактирование существующего сообщения с инлайн-кнопками
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Поставь ударение❌❌❌",
                                  reply_markup=markup)


# Обработчик коллбэка для инлайн-кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """
    Обработчик коллбэка для инлайн-кнопок. Обрабатывает ударение в слове и обновляет статистику.

    :param call: Объект коллбэка от пользователя.
    """
    with db_session.create_session() as db_sess:
        user = db_sess.query(User).filter(User.tg_id == call.from_user.id).first()

        if call.message:
            # Проверяем, совпадает ли выбор пользователя с ударением в слове
            if call.data == user.slovo:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=user.slovo + " ✅",
                                      reply_markup=None)
                # Обновляем статистику при правильном ответе
                user.error = 0
                user.balance += 1
                user.good += 1
                db_sess.commit()
                game(user.tg_id)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="❌❌❌",
                                      reply_markup=None)
                # Обновляем статистику при неправильном ответе
                if user.error != 1:
                    user.balance -= 1
                    user.bad += 1
                user.error = 1
                db_sess.commit()
                game(user.tg_id, call=call)


# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def send_text(message):
    """
    Обработчик текстовых сообщений. Обрабатывает команды пользователя и предоставляет информацию.

    :param message: Объект сообщения от пользователя.
    """
    with db_session.create_session() as db_sess:
        user = db_sess.query(User).filter(User.tg_id == message.from_user.id).first()

        # Обрабатываем команды пользователя
        if message.text.lower() == "начать❤️":
            game(message.from_user.id)
        elif message.text.lower() == "счёт🧩":
            bot.send_message(message.chat.id, f"Счёт: {user.balance}🧩")
        elif message.text.lower() == "сброс⚠️":
            # Сбрасываем данные пользователя
            user.balance = 0
            user.error = 0
            user.good = 0
            user.bad = 0
            user.slovo = ""
            db_sess.commit()
            bot.send_message(message.chat.id, "Данные удалены")
        elif message.text.lower() == "статистика📊":
            # Отправляем статистику пользователя
            bot.send_message(message.chat.id, f"Правильно: {user.good}✅")
            bot.send_message(message.chat.id, f"Неправильно: {user.bad}❌")
        elif message.text.lower() == "топ🏅":
            # Отправляем топ-10 пользователей
            top(message)
        else:
            # Ответ на неизвестную команду
            bot.send_message(message.chat.id, "Я еще молодой бот👾, и я не знаю такой команды 👉👈")


# Запуск бота
if __name__ == '__main__':
    # Инициализация базы данных и запуск бота
    db_session.global_init("db/mars.db")
    bot.polling()

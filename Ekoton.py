import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import datetime
import schedule
import time
from threading import Thread

def Weather():
    html = requests.get("https://www.google.com/search?q=weatherMoscow").content
    soup = BeautifulSoup(html, 'html.parser')

    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    str_ = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

    data = str_.split('\n')
    time = data[0]
    sky = data[1]

    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})

    strd = listdiv[5].text
    pos = strd.find('Wind')
    other_data = strd[pos:]

    return (temp, time, sky, other_data)

class Event():
    def __init__(self):
        self.Name = ""
        self.Link = ""
        self.Description = ""
        self.Date = None
        self.Location = ""
        self.Theme = ""
        self.Coords = []

class User():
    def __init__(self, id):
        self.UserId = id
        self.Mailing = False
        self.Themes = []
        self.ThemeSelect = False
        self.EventWatching = False

Users = {}
Themes = ["Наука", "Утилизация", "Экопитание"]
Events = []

Events.append(Event())
Events.append(Event())
Events[0].Name = "EVENT 1"
Events[0].Date = datetime.datetime(2024,1,1,12,0,0)
Events[0].Coords = [59.938924, 30.315311]
Events[0].Theme = "Наука"
Events[1].Name = "EVENT 2"
Events[1].Date = datetime.datetime(2024,1,1,12,0,0)
Events[1].Coords = [59.938924, 30.315311]

Greeting = " Экоактивисты Москвы, у вас есть шанс изменить мир! 🌿\
Присоединяйтесь к мероприятиям, которые вдохновляют на заботу о природе! Откройте для себя уникальные события: от зеленых ярмарок до мастер-классов по устойчивому образу жизни. Узнайте, как внести свой вклад в охрану окружающей среды и познакомьтесь с единомышленниками. \
Не пропустите возможность стать частью экологической революции в столице! 🌍✨ \
Запишитесь на мероприятия уже сегодня и станьте агентом перемен!"

Help = '<b>Помощь</b> 🌱 \
\nДобро пожаловать в нашего бота, который поможет вам быть в курсе экологических событий в Москве! 🌍\
\n\n<b>Как это работает:</b>\
\n1. Подписка на события: Просто нажмите кнопку "Подписаться", и вы будете получать уведомления о ближайших экологических мероприятиях, акциях и инициативных группах.\
\n2. События: Получите информацию о ближайших событиях на сегоднящнюю дату, ближайший месяц или на определенную дату.\
\n3. Темы событий: Вы можете выбрать интересующие вас темы и получать информацию только о тех событиях, которые вам интересны.\
\n\n<b>Часто задаваемые вопросы:</b> ❓\
\n- Как отписаться от уведомлений? Для этого просто нажмите кнопку "Отписаться" в меню.\
\n- Как часто обновляются события? Мы стараемся обновлять информацию ежедневно, чтобы вы всегда были в курсе актуальных мероприятий.\
\n\nСпасибо, что заботитесь об экологии вместе с нами! 🌿'

Subscribe = "🎉 Спасибо за подписку! 🌿\
\n\
\nВы успешно подписались на рассылку экологических событий в Москве! Теперь вы будете получать уведомления о ближайших мероприятиях, акциях и инициативных группах. 📅✨\
\n\
\nСледите за нашими обновлениями и присоединяйтесь к нам в заботе о природе! 🌍💚"

Discribe = "🚫 Вы отписались от рассылки! 😢\
\n\
\nМы сожалеем, что вы решили уйти. Если у вас есть отзывы или пожелания, пожалуйста, дайте нам знать! 💬\
\n\
\nЕсли вы передумали, вы всегда можете подписаться снова. Мы будем рады видеть вас среди наших читателей! 🌿💚\
\n\
\nСпасибо, что были с нами! 🌍✨"

bot = telebot.TeleBot('6854680839:AAE9UTXS8sA_VbVTDuoGkL5HpgXMmziL8_M', parse_mode="HTML")

def MoreEventInfo(Event, user):
    Mes = f"<b>{Event.Name}</b>\n"
    Mes += f"Тема события: {Event.Theme}\n"
    Mes += f"Дата проведения события: {Event.Date}\n"
    Mes += f"Место проведения: {Event.Location}\n"
    Mes += f"\n<b>Подробная информация:</b>\n"
    Mes += f"{Event.Description}\n"
    Mes += f"\nСсылка на событие: {Event.Link}\n"
    bot.send_message(user, Mes, reply_markup=MainMenu(user))
    bot.send_location(user, Event.Coords[0], Event.Coords[1])

def MainMenu(user):
    global Users
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("❓ Помощь")
    btn2 = types.KeyboardButton("⛅ Погода")
    btn3 = types.KeyboardButton("📅 События")
    btn4 = types.KeyboardButton("✅ Подписаться") if not Users[user].Mailing else types.KeyboardButton("❌ Отписаться")
    btn5 = types.KeyboardButton("⚙ Настроить темы")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user.id
    if user not in Users.keys():
        Users[user] = User(user)
    bot.send_message(user, Greeting, reply_markup=MainMenu(user))

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global ThemeSelect
    user = message.from_user.id
    if user not in Users.keys():
        Users[user] = User(user)
    if message.text == "❓ Помощь":
        bot.send_message(message.from_user.id, Help)
    if message.text == "⛅ Погода":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        temp, time, sky, other_data = Weather()

        Mes = f"Сегодня, {time} в Москве {sky}.\n Температура {temp}"

        bot.send_message(message.from_user.id, Mes)
    if message.text == "↪ Назад":
        Users[user].EventWatching = False
        Users[user].ThemeSelect  = False
        start(message)
    if message.text == "✅ Подписаться":
        Users[user].Mailing = True
        bot.send_message(message.from_user.id, Subscribe, reply_markup=MainMenu(user))
    if message.text == "❌ Отписаться":
        Users[user].Mailing = False
        bot.send_message(message.from_user.id, Discribe, reply_markup=MainMenu(user))

    if message.text == "✅ Сохранить":
        Users[user].ThemeSelect  = False
        start(message)

    if message.text == "⚙ Настроить темы":
        Users[user].ThemeSelect = True
        Mes = "<b>Список доступных тем:</b>\n"
        for i in enumerate(Themes):
            Mes += str(i[0]+1) + ") "
            Mes += i[1]
            Mes += " ✅ " if i[1] in Users[user].Themes else " ❌ "
            Mes += "\n"
        Mes += "Напишите номер темы для подписки\отписки от нее"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn4 = types.KeyboardButton("✅ Сохранить")
        markup.add(btn4)

        bot.send_message(message.from_user.id, Mes, reply_markup=markup)

    if Users[user].ThemeSelect and message.text.isdigit():
        try:
            Number = int(message.text)
            Ind = Number-1
            if Themes[Ind] not in Users[user].Themes:
                Users[user].Themes.append(Themes[Ind])
            else:
                Users[user].Themes.remove(Themes[Ind])

            Mes = "<b>Список доступных тем:</b>\n"
            for i in enumerate(Themes):
                Mes += str(i[0] + 1) + ") "
                Mes += i[1]
                Mes += " ✅ " if i[1] in Users[user].Themes else " ❌ "
                Mes += "\n"
            Mes += "Напишите номер темы для подписки\отписки от нее"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn4 = types.KeyboardButton("✅ Сохранить")
            markup.add(btn4)

            bot.send_message(message.from_user.id, Mes, reply_markup=markup)
        except:
            bot.send_message(message.from_user.id, "Произошла ошибка!")

    if message.text == "📅 События":
        Users[user].EventWatching = True
        Mes = "<b>Ближайшие события:</b>\n"
        for i in enumerate(Events):
            Mes += str(i[0]+1) + ") "
            Mes += str(i[1].Date) + " - " + i[1].Name
            Mes += "\n"
        Mes += "Напишите номер события чтобы узнать подробнее"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("↪ Назад")
        markup.add(btn1)

        bot.send_message(message.from_user.id, Mes, reply_markup=markup)

    if Users[user].EventWatching and message.text.isdigit():
        try:
            Number = int(message.text)
            Ind = Number - 1

            MoreEventInfo(Events[Ind], user)

            Mes = "<b>Ближайшие события:</b>\n"
            for i in enumerate(Events):
                Mes += str(i[0] + 1) + ") "
                Mes += str(i[1].Date) + " - " + i[1].Name
                Mes += "\n"
            Mes += "Напишите номер события чтобы узнать подробнее"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("↪ Назад")
            markup.add(btn1)

            bot.send_message(message.from_user.id, Mes, reply_markup=markup)
        except:
            bot.send_message(message.from_user.id, "Произошла ошибка!")

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(10)

def function_to_run():
    print("FUNC")
    for Ev in Events:
        for Us in Users.keys():
            if Ev.Theme in Users[Us].Themes:
                MoreEventInfo(Ev, Us)
if __name__ == "__main__":
    schedule.every().day.at("12:00").do(function_to_run)
    Thread(target=schedule_checker).start()
    bot.polling(none_stop=True, interval=0)
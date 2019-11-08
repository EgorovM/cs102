import requests
import config
import telebot
import datetime
from bs4 import BeautifulSoup

config = config.Config("bot.cfg")
telebot.apihelper.proxy = {'https':'socks5h://87.228.37.246:9999'}
bot = telebot.TeleBot(config.access_token)
days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)

    print(url)
    response = requests.get(url, verify=False)
    web_page = response.text

    return web_page


def parse_schedule_for_a_week(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")

    schedule_table = soup.find("table", attrs={"id": f"{days.index(day)+1}day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list

def parse_near_schedule(message, web_page, day, is_next_day = 0):
    curr_hour, curr_minute = datetime.datetime.today().hour, datetime.datetime.today().minute

    times_lst, locations_lst, lessons_lst = parse_schedule_for_a_week(web_page, day)

    for ind in range(len(times_lst)):
        hour, minute = times_lst[ind].split("-")[0].split(":")
        day =
        if int(hour) > curr_hour or (int(hour) == curr_hour and int(minute) >= curr_minute) or (is_next_day):
            return times_lst, locations_lst, lessons_lst

    parse_near_schedule(message, web_page, days[days.index(day)+1], 1)

@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    command , group = message.text.split()

    if command[1:] != "sunday":
        web_page = get_page(group.upper())
        times_lst, locations_lst, lessons_lst = \
            parse_schedule_for_a_week(web_page, command[1:])
        resp = ''

        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>,\n {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "Отдыхай)")

@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _ , group = message.text.split()
    day = days[ datetime.datetime.today().weekday()]

    if day != "sunday":
        web_page = get_page(group.upper())
        parse_data = parse_near_schedule(message,web_page,day)

        times_lst, locations_lst, lessons_lst = parse_near_schedule(message,web_page,day)

        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>,\n {}, {}\n'.format(time, location, lession)

        bot.send_message(message.chat.id, resp, parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "Отдыхай)")

@bot.message_handler(commands=['tomorrow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    new_message = message.text.split()
    next_day = days[(datetime.datetime.today().weekday()+1)%7]
    new_message[0] = "/" + next_day

    message.text = " ".join(new_message)
    get_schedule(message)



@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _ , group = message.text.split()
    web_page = get_page(group.upper())
    resp = ''

    for day in days:
        times_lst, locations_lst, lessons_lst = \
            parse_schedule_for_a_week(web_page, day)

        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>,\n {}, {}\n'.format(time, location, lession)

    bot.send_message(message.chat.id, resp, parse_mode="HTML")

@bot.message_handler(commands=['start', 'help'])
def get_all_schedule(message):
    msg = ""
    if 'start' in message.text:
        msg = 'Добро пожаловать!'
    bot.send_message(message.chat.id, msg+
    '''
    Доступные команды:
    ''')


if __name__ == '__main__':
    bot.polling(none_stop=True)

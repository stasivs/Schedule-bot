from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, Dispatcher, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import json

with open('data.json') as json_file:
    schedules = json.load(json_file)


class Bot:
    def __init__(self):
        self.weekend = ["понедельник", "вторник", "среда", "четверг", "пятница"]
        self.pair_time = ["8:30 - 10:00", "10:10 - 11:40", "11:50 - 13:20", "13:30 - 15:00", "15:10 - 16:40", "16:50 - 18:20"]
        self.parity = ["ч", "н"]
        with open("db.json", "r", encoding="utf8") as db:
            self.data = json.load(db)

    def start(self, bot, update):
        update.message.reply_text("Добро пожаловать в бота для выдачи рассписания,\n"
                                  "Если вы еще не регистрировались используйте комманду\n"
                                  "/reg, а если нет, то чтобы получить расписание на день, то\n"
                                  "Введите в формате 'День недели Н/Ч'")

    def registration_start(self, bot, update):
        update.message.reply_text("Привет! Укажи свой институт, курс, группу, подгруппу, в формате\n"
                                  "Институт курс-группа подгруппа\n"
                                  "Пример:\n"
                                  "ИФО 1-1 1")
        return 1

    def registration_end(self, bot, update):
        text = update.message.text.split()
        # Проверка на формат
        try:
            institute, course, group, subgroup = text[0], *text[1].split("-"), text[2]
        except Exception:
            update.message.reply_text("Неправильный формат данных")
            return 1

        key = institute.lower() + " " + course + " " + group
        data = {"institute": institute, "course": course, "group": group, "subgroup": subgroup}

        # Проверка на корректность
        if key in schedules and subgroup in ["1", "2"]:
            self.data[str(update.message.chat.id)] = data
            with open("db.json", "w", encoding="utf8") as db:
                json.dump(self.data, db)

            update.message.reply_text("Регистрация успешно пройдена")

            return ConversationHandler.END
        elif subgroup not in ["1", "2"] and key not in schedules:
            update.message.reply_text("У нас отсутствует информация о таком направлении в бд\n"
                                      "Неправильно введена подгруппа (1 или 2)")
        elif key not in schedules:
            update.message.reply_text("У нас отсутствует информация о таком направлении в бд")
        elif subgroup not in ["1", "2"]:
            update.message.reply_text("Неправильно введена подгруппа (1 или 2)")
        return 1

    def stop(self, bot, update):
        update.message.reply_text('Регистрация прервана')
        return ConversationHandler.END

    def schedule(self, bot, update):
        id = str(update.message.chat.id)
        if id in self.data:
            text = update.message.text.lower().split()
            # Проверка на формат
            if text[0] in self.weekend and text[1] in self.parity:
                user_data = self.data[id]
                # Ключ / Подгруппа
                key, subgroup = user_data["institute"].lower() + " " + user_data["course"] + " " + user_data["group"], int(user_data["subgroup"]) - 1
                # День / Четность
                day, parity = text[0].capitalize(), self.parity.index(text[1])
                # Итоговое расписание
                schedule = schedules[key][subgroup][day][parity]

                # Итоговый формат расписания
                res = ""
                update.message.reply_text("Вот ваше расписание:")
                for number, lesson in enumerate(schedule):
                    if not lesson:
                        lesson = "Ничего"
                    res += "{} Пара {}:\n{}\n\n".format(number + 1, self.pair_time[number], lesson.replace("\n", " "))
                update.message.reply_text(res)
            else:
                update.message.reply_text("Была допущена ошибка")
        else:
            update.message.reply_text("Сначала вам необходимо пройти регистрацию.\n"
                                      "Выполните /reg")


if __name__ == "__main__":
    token = "1313546180:AAFhVROyewnsp2FjXZQO7GuMFexs1J_DQ0o"
    updater = Updater(token)
    dp = updater.dispatcher

    bot = Bot()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('reg', bot.registration_start)],
        states={
            1: [MessageHandler(Filters.text, bot.registration_end)],
        },
        fallbacks=[CommandHandler('stop', bot.stop)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('start', bot.start))
    dp.add_handler(MessageHandler(Filters.text, bot.schedule))

    updater.start_polling()
    print("Started")
    updater.idle()
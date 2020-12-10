#допилить другой язык, таймер, ответы на неверно введеный текст, ссылки на дистант, сброс всех параметров, плашечку с информацией
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, Dispatcher, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import json
import requests
import Converter

with open('data.json') as json_file:
    data = json.load(json_file)


#class Bot:
    def __init__(self):
        pass

    def start(self, update):
        update.message.reply_text("ку заведомо знаем, что с ИСА скажи свой курс(хочешь закончить напиши /stop)")
        return 1

    def first(self, update, user_data):
        update.message.reply_text('Хорошо, напиши свою группу')
        course = update.message.text
        user_data['course'] = course
        return 2

    def second(self, update, user_data):
        update.message.reply_text('Хорошо, напиши свою подгруппу')
        group = update.message.text
        user_data['group'] = group
        return 3

    def third(self, update, user_data):
        update.message.reply_text('Хорошо, напиши нужный день недели')
        undergroup = update.message.text
        user_data['undergroup'] = undergroup
        return 4

    def fourth(self, update, user_data):
        update.message.reply_text('Хорошо, напиши четность недели, где 0 - нечетная, 1 - четная')
        dayofweek = update.message.text
        return 5

    def five(self, update):
        update.message.reply_text('Держи твое расписание! Ждем снова...')
        parity = update.message.text
        print(data['ИСА ' + course + group + ' (Б) (оч.ф.о., 08.03.01 )'][undergroup][dayofweek][parity])
        return ConversationHandler.END

# для остановки конверсейшн бота
    def stop(self, update):
        update.message.reply_text('Был рад помочь!')
        return ConversationHandler.END


if __name__ == "__main__":
    token = ""  # bot token
    updater = Updater('token')
    dp = updater.dispatcher

    #bot = Bot()


# сам конверсейшн с ботом
conersation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        1: [MessageHandler(Filters.all, first)],
        2: [MessageHandler(Filters.all, second)],
        3: [MessageHandler(Filters.all, third)],
        4: [MessageHandler(Filters.all, fourth)],
        5: [MessageHandler(Filters.all, five)],

        },

    fallbacks=[CommandHandler('stop', stop)]
)


dp.add_handler(conv_handler)
dp.add_handler(CommandHandler('stop', stop))
dp.add_handler(CommandHandler('start', start))


updater.start_polling()

updater.idle()


dp = updater.dispatcher




#допилить другой язык, таймер, ответы на неверно введеный текст, ссылки на дистант, сброс всех параметров
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, Dispatcher, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import json
import requests
import Converter

with open('data.json') as json_file:
    data = json.load(json_file)

# узнаем институт, направление, курс, группу, подгруппу (Узнаем имя для обращения)скидываем расп на нужн день
# реализовывать будем кнопками, если подгруппы нет выдаем null
class Bot:
    def __init__(self):
        pass


markup = ''
markup2 = ''
markup3 = ''
markup4 = ''
markup5 = ''
markup6 = ''
markup7 = ''
markup8 = ''


#в функциях ниже мы узнаем всю инфу(почти)
def start(self, bot, update):
    update.message.reply_text("ку выбери институт(хочешь закончить напиши /stop)")
    reply_keyboard = [['ИФО', 'ИСА', 'МФ'],
                      ['ИГЭС', 'ИИЭСМ'],
                      ['ИЭУИС', 'ИДО']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    #действием ниже(оно повторяется почти везде) я хотел сохранить информацию о пользователе, чтобы он не вводил это повторно
    inst = update.message.text
    user_data['inst'] = inst

    return 1


def first(bot, update, userdata):
    update.message.reply_text('Чудесный институт:) А теперь выбери из' + data[markup] + 'свою программу обучения')
    #или мне плохо или я не выкупаю как достать и вставить их в клаву поэтмоу оставлю так пока что
    reply_keyboard2 = [[ flow ]]

    markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)
    flow = update.message.text
    user_data['flow'] = flow
    return 2


def second(bot, update, userdata):
    update.message.reply_text('а теперь скажи твой уровень обучения' + data[markup2])
    #аналогичный движ не понимаю как достать
    reply_keyboard3 = [[ graduate ]]

    markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True)
    graduate = update.message.text
    user_data['graduate'] = graduate
    return 3


def third(bot, update, userdata):
    update.message.reply_text('назови курс' + data[markup3])
    # аналогичный движ не понимаю как достать
    reply_keyboard4 = [[ course ]]

    markup4 = ReplyKeyboardMarkup(reply_keyboard4, one_time_keyboard=True)
    course = update.message.text
    user_data['course'] = course
    return 4


def fourth1(bot, update, userdata):
    update.message.reply_text('назови группу из' + data[markup4])
        # аналогичный движ не понимаю как достать
    reply_keyboard5 = [[ groups ]]

    markup5 = ReplyKeyboardMarkup(reply_keyboard5, one_time_keyboard=True)
    return 5


def fourth(bot, update, userdata):
    update.message.reply_text('назови группу из' + data[markup5])
        # аналогичный движ не понимаю как достать
    reply_keyboard6 = [[ groups ]]

    markup6 = ReplyKeyboardMarkup(reply_keyboard6, one_time_keyboard=True)
    group = update.message.text
    user_data['group'] = group
    return 6

def five(bot, update, userdata):
    update.message.reply_text('назови подгруппу из' + data[markup6])
        # аналогичный движ не понимаю как достать
    reply_keyboard7 = [[ undergroups ]]

    markup7 = ReplyKeyboardMarkup(reply_keyboard7, one_time_keyboard=True)
    undergroup = update.message.text
    user_data['undergroup'] = undergroup
    return 7

def six(bot, update, userdata):
    update.message.reply_text('назови группу из' + data[markup7])
        # аналогичный движ не понимаю как достать из твоего, это написал сам
    reply_keyboard8 = [['Понедельник', 'Вторник', 'Среда'],
                       ['Четверг', 'Пятница']]

    markup8 = ReplyKeyboardMarkup(reply_keyboard8, one_time_keyboard=True)
    update.message.reply_text(тут должно быть распиание на указаный юзером день)

    return ConversationHandler.END


#для остановки конверсейшн бота
def stop(bot, update):
    update.message.reply_text('Был рад помочь!')
    return ConversationHandler.END


if __name__ == "__main__":
    token = "1313546180:AAFhVROyewnsp2FjXZQO7GuMFexs1J_DQ0o" #bot token
    updater = Updater('1313546180:AAFhVROyewnsp2FjXZQO7GuMFexs1J_DQ0o')
    dp = updater.dispatcher

    bot = Bot()


#сам конверсейшн с ботом
ConvHandler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        1: [MessageHandler(first)],
        2: [MessageHandler(second)],
        3: [MessageHandler(third)],
        4: [MessageHandler(fourth1)],
        5: [MessageHandler(fourth)],
        6: [MessageHandler(five)],
        7: [MessageHandler(six)],

        },

    fallbacks = [CommandHandler('stop', stop)]
)


dp.add_handler(ConvHandler)
dp.add_handler(CommandHandler('stop', stop))
dp.add_handler(CommandHandler('start', start))


updater.start_polling()

#    print("Привет! Я - бот в котором ты всегда сможешь узнать расписание!")

updater.idle()


dp = updater.dispatcher

#


from telegram.ext import Updater, MessageHandler, CommandHandler


class Bot:
    def __init__(self):
        pass

    def start(self, bot, update):
        bot.sendMessage("Hi!")


if __name__ == "__main__":
    token = ""
    updater = Updater(token)
    dp = updater.dispatcher

    bot = Bot()

    start_handler = CommandHandler("start", bot.start)
    dp.add_handler(start_handler)

    updater.start_polling()
    print("Started")
    updater.idle()

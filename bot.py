import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}, I am  telegram chat analytics bot')


def main() -> None:
    updater = Updater(os.getenv('TOKEN'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

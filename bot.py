import os
from telegram import Update, Document, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler

from analyzer.tools import load_json, chat_info


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}, I am  telegram chat analytics bot')


def handle_document(update: Update, context: CallbackContext) -> None:
    document = update.message.document
    if document.mime_type == 'application/json':
        file_id = document.file_id
        file = context.bot.get_file(file_id)
        file_path = file.download()
        data = load_json(file_path)
        if data:

            keyboard = [
                [InlineKeyboardButton("Chat Information", callback_data='chat_info')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Please select a functionality:', reply_markup=reply_markup)
            context.user_data['file_path'] = file_path
        else:
            update.message.reply_text("Failed to process the JSON file.")
    else:
        update.message.reply_text("Only JSON files are supported. Please send a JSON file.")


def button_press(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'chat_info':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                chat_info_dict = chat_info(data)
                chat_info_text = (
                    f"Chat Name: {chat_info_dict['name']}\n"
                    f"Chat Type: {chat_info_dict['type']}\n"
                    f"Chat ID: {chat_info_dict['id']}\n"
                    f"Messages Count: {chat_info_dict['messages_count']}"
                )
                query.message.reply_text(chat_info_text)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    else:
        query.message.reply_text("Invalid option selected.")


def main() -> None:
    updater = Updater(os.getenv('TOKEN'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))
    dispatcher.add_handler(CallbackQueryHandler(button_press))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

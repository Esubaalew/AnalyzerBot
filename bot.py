import os
from datetime import datetime, timedelta

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
    CallbackQueryHandler
)

from analyzer.tools import (
    load_json,
    chat_info,
    get_oldest_message,
    get_latest_message,
    get_senders,
    get_forwarders,
    count_forwarded_messages,
    get_forward_sources,
    count_replies, get_repliers,
    get_editors, count_edited_messages,
    get_most_common_words,
    get_most_active_hours,
    get_most_active_weekdays,
    get_most_active_months,
    get_most_active_year,
get_most_active_months_all_time
)


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
                [InlineKeyboardButton("Oldest Message", callback_data='oldest_message')],
                [InlineKeyboardButton("Latest Message", callback_data='latest_message')],
                [InlineKeyboardButton("RankSenders", callback_data='rank_senders')],
                [InlineKeyboardButton("RankForwarders", callback_data='rank_forwarders')],
                [InlineKeyboardButton("ForwardSources", callback_data='forward_sources')],
                [InlineKeyboardButton("RankRepliers", callback_data='rank_repliers')],
                [InlineKeyboardButton("RankEditors", callback_data='rank_editors')],
                [InlineKeyboardButton("MostCommonWords", callback_data='most_common_words')],
                [InlineKeyboardButton("MostActiveHours", callback_data='most_active_hours')],
                [InlineKeyboardButton("MostActiveWeekdays", callback_data='most_active_weekdays')],
                [InlineKeyboardButton("MostActiveMonths", callback_data='most_active_months')],
                [InlineKeyboardButton("MostActiveYear", callback_data='most_active_year')],
                [InlineKeyboardButton("MostActiveMonthsAllTime", callback_data='most_active_months_all_time')]
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
    elif query.data == 'oldest_message':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                oldest_date = get_oldest_message(data)['date']
                formatted_date = f"{oldest_date['day']}/{oldest_date['month']}/{oldest_date['year']}"
                query.message.reply_text(f"The oldest message in the chat was sent on {formatted_date}.")
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'latest_message':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                latest_date = get_latest_message(data)['date']
                formatted_date = f"{latest_date['day']}/{latest_date['month']}/{latest_date['year']}"
                query.message.reply_text(f"The latest message in the chat was sent on {formatted_date}.")
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'rank_senders':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                senders = get_senders(data)
                senders_text = "Rank of Senders:\n"
                for index, sender in enumerate(senders, start=1):
                    senders_text += f"{index}. {sender['sender']} - Messages: {sender['messages']}\n"
                query.message.reply_text(senders_text)

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'rank_forwarders':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                all_forwarders = count_forwarded_messages(data)
                forwarders = get_forwarders(data)
                forwarders_text = "Rank of Forwarders:\n"
                for index, (forwarder, count) in enumerate(forwarders.items(), start=1):
                    forwarders_text += f"{index}. {forwarder} - Forwarded Messages: {count}\n"
                reply_text = f"Total forwarded messages: {all_forwarders}\n\n{forwarders_text}"
                query.message.reply_text(reply_text)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'forward_sources':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                forward_sources = get_forward_sources(data)
                forward_sources_text = "Rank of Forward Sources:\n"
                for index, (forward_source, count) in enumerate(forward_sources.items(), start=1):
                    forward_sources_text += f"{index}. {forward_source} - Forwarded Messages: {count}\n"
                query.message.reply_text(forward_sources_text)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'rank_repliers':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                total_repliers = count_replies(data)
                repliers_ranking = get_repliers(data)
                repliers_text = f"Total replies: {total_repliers}\n\nRank of Repliers:\n"
                for index, (replier, count) in enumerate(repliers_ranking.items(), start=1):
                    repliers_text += f"{index}. {replier} - Replies Count: {count}\n"
                query.message.reply_text(repliers_text)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'rank_editors':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                total_edited_messages = count_edited_messages(data)
                editors_ranking = get_editors(data)
                editors_text = f"Total edited messages: {total_edited_messages}\n\nRank of Editors:\n"
                for index, (editor, count) in enumerate(editors_ranking.items(), start=1):
                    editors_text += f"{index}. {editor} - Edited Messages Count: {count}\n"
                query.message.reply_text(editors_text)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'most_common_words':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                most_common_words_list = get_most_common_words(data)
                words_text = "Top 10 most common words:\n"
                words_text += "{:<3} {:<15} {:<10}\n".format("No.", "Word", "Occurrence")
                for index, word_info in enumerate(most_common_words_list, start=1):
                    words_text += f"{index:<3} {word_info['word']:<15} {word_info['occurrence']:<10}\n"
                query.message.reply_text(words_text)

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'most_active_hours':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                active_hours = get_most_active_hours(data)
                hours, counts = zip(*active_hours)
                ethiopian_hours = [(datetime.strptime(str(hour), '%H') + timedelta(hours=3)).strftime('%I %p') for hour
                                   in hours]

                hours_text = "Most active hours:\n"
                for rank, (hour, count) in enumerate(zip(ethiopian_hours, counts), start=1):
                    hours_text += f"{rank}. {hour}: {count} Messages\n"

                query.message.reply_text(hours_text)

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'most_active_weekdays':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                active_weekdays = get_most_active_weekdays(data)

                weekdays_text = "Most active weekdays:\n\n"
                for weekday, count in active_weekdays:
                    weekdays_text += f"{weekday}: {count} Messages\n"
                query.message.reply_text(weekdays_text)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'most_active_months':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                active_months = get_most_active_months(data)

                active_months = active_months[:100]

                months_text = "Most active months:\n\n"
                for month, count in active_months:
                    months_text += f"{month}: {count} Messages\n"
                query.message.reply_text(months_text)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'most_active_year':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                active_years = get_most_active_year(data)

                active_years = active_years[:100]

                years_text = "Most active years:\n\n"
                for year, count in active_years:
                    years_text += f"{year}: {count} Messages\n"
                query.message.reply_text(years_text)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'most_active_months_all_time':
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                active_months_list = get_most_active_months_all_time(data)

                months_text = "Most active months of all time:\n"
                for index, month_info in enumerate(active_months_list, start=1):
                    months_text += f"{index}. {month_info['name']}: {month_info['messages']}\n"
                query.message.reply_text(months_text)
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

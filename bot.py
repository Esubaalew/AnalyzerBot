import os
import time
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
    get_most_active_months_all_time,
    get_most_active_months_by_year
)
from analyzer.visuals.active_senders import (visualize_bar_chart,
                                             visualize_pie_chart,
                                             visualize_area_chart,
                                             visualize_line__chart,
                                             visualize_vertical_chart
                                             )
from analyzer.visuals.active_weekdays import (
    visualize_most_active_weekdays_bar,

    visualize_most_active_weekdays_pie)

from analyzer.visuals.forwarders import (
    visualize_forwarders_vertical_bar_chart,
    visualize_forwarders_bar_chart,
    visualize_forwarders_line_chart,
    visualize_forwarders_pie_chart,
    visualize_forwarders_area_chart
)

from analyzer.visuals.repliers import (
    visualize_bar_chart_repliers,
    visualize_vertical_bar_chart_repliers,
    visualize_pie_chart_repliers,
    visualize_area_chart_repliers,
    visualize_line_chart_repliers
)
from analyzer.visuals.editors import (
    visualize_pie_chart_editors,
    visualize_vertical_bar_chart_editors,
    visualize_bar_chart_editors,
    visualize_area_chart_editors,
    visualize_line_chart_editors
)

from analyzer.visuals.forward_sources import *
from analyzer.visuals.common_words import visualize_most_common_words
from analyzer.visuals.active_hours import *
from analyzer.visuals.active_months import *
from analyzer.visuals.active_years import *


def start(update: Update, context: CallbackContext) -> None:
    user_first_name = update.effective_user.first_name

    tools_list = [
        "1. Chat Info",
        "2. Oldest Message",
        "3. Latest Message",
        "4. Rank Senders",
        "5. Rank Forwarders",
        "6. Forward Sources",
        "7. Rank Repliers",
        "8. Rank Editors",
        "9. Common Words",
        "10. Active Hours",
        "11. Active Weekdays",
        "12. Active Months",
        "13. Active Years",
        "14. Months All Time",
        "15. Months By Year"
    ]

    tools_message = "\n".join(tools_list)

    update.message.reply_text(
        f'Hello {user_first_name}, I am Liyu Bot, a Telegram chat analytics bot.\n'
        f'You can use the following tools to analyze and visualize the Telegram groups:\n'
        f'{tools_message}'
    )


def help(update: Update, context: CallbackContext) -> None:
    message = "Go to your any  telegram group on your desktop and export the chat history as a JSON file. " \
              "Then send the JSON file to the bot and choose the functionality you want to perform."
    update.message.reply_text(message)


def unknown_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Sorry, I didn't understand that command.")


def unknown_text(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Sorry, I didn't understand that text.")


def filter_photos(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("I guess this pic is good. Please send a JSON file instead.")


def filter_videos(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("What is this video? Please send a JSON file instead.")


def filter_audios(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Audio,  yeah? Please send a JSON file instead.")


def filter_voice(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("This might be your voice ah? Please send a JSON file instead.")


def filter_location(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please send a JSON file instead, I guess this is your location.")


def filter_contact(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("OH!! is this your contact? Please send a JSON file instead.")


def filter_sticker(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("What is this sticker? Please send a JSON file instead.")


def filter_poll(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("A poll? Please send a JSON file instead.")


def handle_document(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    document = update.message.document
    if document.file_size > 20971520:
        update.message.reply_text("The file size exceeds the limit. Please upload a file smaller than 20 MB.")
        return
    if document.mime_type == 'application/json':

        file_id = document.file_id
        file = context.bot.get_file(file_id)
        file_path = file.download()
        data = load_json(file_path)
        if data:
            buttons = [
                InlineKeyboardButton("ChatInfo", callback_data='chat_info'),
                InlineKeyboardButton("OldestMessage", callback_data='oldest_message'),
                InlineKeyboardButton("LatestMessage", callback_data='latest_message'),
                InlineKeyboardButton("RankSenders", callback_data='rank_senders'),
                InlineKeyboardButton("RankForwarders", callback_data='rank_forwarders'),
                InlineKeyboardButton("ForwardSources", callback_data='forward_sources'),
                InlineKeyboardButton("RankRepliers", callback_data='rank_repliers'),
                InlineKeyboardButton("RankEditors", callback_data='rank_editors'),
                InlineKeyboardButton("CommonWords", callback_data='most_common_words'),
                InlineKeyboardButton("ActiveHours", callback_data='most_active_hours'),
                InlineKeyboardButton("ActiveWeekdays", callback_data='most_active_weekdays'),
                InlineKeyboardButton("ActiveMonths", callback_data='most_active_months'),
                InlineKeyboardButton("ActiveYears", callback_data='most_active_year'),
                InlineKeyboardButton("MonthsAllTime", callback_data='most_active_months_all_time'),
                InlineKeyboardButton("MonthsByYear", callback_data='most_active_months_by_year')
            ]

            keyboard = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
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
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
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
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
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
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
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
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                senders = get_senders(data)[:100]
                senders_text = "Rank of Top 100 Senders:\n"
                for index, sender in enumerate(senders, start=1):
                    senders_text += f"{index}. {sender['sender']} - Messages: {sender['messages']}\n"
                keyboard = [
                    [InlineKeyboardButton("Visualize Senders", callback_data='visualize_senders')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text(senders_text, reply_markup=reply_markup, )

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'rank_forwarders':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                all_forwarders = count_forwarded_messages(data)
                forwarders = get_forwarders(data)
                forwarders_text = "Rank of Top 100 Forwarders:\n"
                for index, (forwarder, count) in enumerate(forwarders.items(), start=1):
                    forwarders_text += f"{index}. {forwarder} - Forwarded Messages: {count}\n"
                reply_text = f"Total forwarded messages: {all_forwarders}\n\n{forwarders_text}"
                keyboard = [
                    [InlineKeyboardButton("Visualize Forwarders", callback_data='visualize_forwarders')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text(reply_text, reply_markup=reply_markup, )

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'forward_sources':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                forward_sources = get_forward_sources(data)
                forward_sources_text = "Rank of Top 100 Forward Sources:\n"
                for index, (forward_source, count) in enumerate(forward_sources.items(), start=1):
                    forward_sources_text += f"{index}. {forward_source} - Forwarded Messages: {count}\n"
                keyboard = [
                    [InlineKeyboardButton("Visualize Sources", callback_data='visualize_sources')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text(forward_sources_text, reply_markup=reply_markup, )

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'rank_repliers':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                total_repliers = count_replies(data)
                repliers_ranking = get_repliers(data)
                repliers_text = f"Total replies: {total_repliers}\n\nRank of Top 100 Repliers:\n"
                for index, (replier, count) in enumerate(repliers_ranking.items(), start=1):
                    repliers_text += f"{index}. {replier} - Replies Count: {count}\n"

                keyboard = [
                    [InlineKeyboardButton("Visualize Repliers", callback_data='visualize_repliers')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text(repliers_text, reply_markup=reply_markup, )

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'rank_editors':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                total_edited_messages = count_edited_messages(data)
                editors_ranking = get_editors(data)
                editors_text = f"Total edited messages: {total_edited_messages}\n\nRank of Top 100 Editors:\n"
                for index, (editor, count) in enumerate(editors_ranking.items(), start=1):
                    editors_text += f"{index}. {editor} - Edited Messages Count: {count}\n"

                keyboard = [
                    [InlineKeyboardButton("Visualize Editors", callback_data='visualize_editors')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text(editors_text, reply_markup=reply_markup)

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'most_common_words':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                most_common_words_list = get_most_common_words(data)
                words_text = "Top 10 most common words:\n"
                words_text += "{:<3} {:<15} {:<10}\n".format("No.", "Word", "Occurrence")
                for index, word_info in enumerate(most_common_words_list, start=1):
                    words_text += f"{index:<3} {word_info['word']:<15} {word_info['occurrence']:<10}\n"

                keyboard = [
                    [InlineKeyboardButton("Visualize Words", callback_data='visualize_words')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text(words_text, reply_markup=reply_markup)

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'most_active_hours':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
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
                keyboard = [
                    [InlineKeyboardButton("Visualize Hours", callback_data='visualize_hours')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text(hours_text, reply_markup=reply_markup, )

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'most_active_weekdays':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                active_weekdays = get_most_active_weekdays(data)

                weekdays_text = "Most active weekdays:\n\n"
                for weekday, count in active_weekdays:
                    weekdays_text += f"{weekday}: {count} Messages\n"
                keyboard = [
                    [InlineKeyboardButton("Visualize Weekdays", callback_data='visualize_weekdays')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text(weekdays_text, reply_markup=reply_markup, )

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'most_active_months':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                active_months = get_most_active_months(data)

                active_months = active_months[:100]

                months_text = "Most active months:\n\n"
                for month, count in active_months:
                    months_text += f"{month}: {count} Messages\n"
                keyboard = [
                    [InlineKeyboardButton("Visualize Months", callback_data='visualize_months')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text(months_text, reply_markup=reply_markup, )

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'most_active_year':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                active_years = get_most_active_year(data)

                active_years = active_years[:100]

                years_text = "Most active years:\n\n"
                for year, count in active_years:
                    years_text += f"{year}: {count} Messages\n"

                keyboard = [
                    [InlineKeyboardButton("Visualize Years", callback_data='visualize_years')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                query.message.reply_text(years_text, reply_markup=reply_markup, )
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'most_active_months_all_time':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                active_months_list = get_most_active_months_all_time(data)

                months_text = "Most active months of all time:\n"
                for index, month_info in enumerate(active_months_list, start=1):
                    months_text += f"{index}. {month_info['name']}: {month_info['messages']}\n"

                keyboard = [
                    [InlineKeyboardButton("Visualize AllTimeMonths", callback_data='visualize_months_all')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text(months_text, reply_markup=reply_markup, )
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'most_active_months_by_year':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                active_months_by_year = get_most_active_months_by_year(data)

                response_text = "Most active months by year:\n"
                for year, months in active_months_by_year.items():
                    response_text += f"\n{year}:\n"
                    for index, month_info in enumerate(months, start=1):
                        response_text += f"    {index}. {month_info['name']}: {month_info['messages']}\n"
                keyboard = [
                    [InlineKeyboardButton("Visualize MonthsByYear", callback_data='visualize_months_year')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text(response_text, reply_markup=reply_markup)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'visualize_senders':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                bar_chart_file = visualize_bar_chart(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(bar_chart_file, 'rb'),
                    caption='Top 10 most active users based on the number of messages they sent.')
                os.remove(bar_chart_file)
                pie_chart_file = visualize_pie_chart(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(pie_chart_file, 'rb'),
                    caption='Proportion of messages sent by each sender using a pie chart.')
                os.remove(pie_chart_file)
                area_chart_file = visualize_area_chart(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(area_chart_file, 'rb'),
                    caption='Area chart ')
                os.remove(area_chart_file)
                line_chart_file = visualize_line__chart(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(line_chart_file, 'rb'), )
                os.remove(line_chart_file)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'visualize_weekdays':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                bar_chart_file = visualize_most_active_weekdays_bar(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(bar_chart_file, 'rb'),
                    caption='The most active weekdays bar chart.')
                os.remove(bar_chart_file)
                pie_chart_file = visualize_most_active_weekdays_pie(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(pie_chart_file, 'rb'),
                    caption='The most active weekdays pie chart.')
                os.remove(pie_chart_file)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'visualize_forwarders':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                bar_chart_file = visualize_forwarders_bar_chart(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(bar_chart_file, 'rb'),
                    caption='The most active forwarders bar chart.')
                os.remove(bar_chart_file)
                pie_chart_file = visualize_forwarders_pie_chart(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(pie_chart_file, 'rb'),
                    caption='The most active forwarders pie chart.')
                os.remove(pie_chart_file)
                line_chart_file = visualize_forwarders_line_chart(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(line_chart_file, 'rb'),
                    caption='The most active forwarders line chart.')
                os.remove(line_chart_file)

                vertical_chart_file = visualize_forwarders_vertical_bar_chart(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(vertical_chart_file, 'rb'),
                    caption='The most active forwarders vertical bar chart.')
                os.remove(vertical_chart_file)

                area_chart_file = visualize_forwarders_area_chart(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(area_chart_file, 'rb'),
                    caption='The most active forwarders area chart.')
                os.remove(area_chart_file)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'visualize_repliers':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                bar_chart_file = visualize_bar_chart_repliers(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(bar_chart_file, 'rb'),
                    caption='The most active repliers bar chart.')
                os.remove(bar_chart_file)

                pie_chart_file = visualize_pie_chart_repliers(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(pie_chart_file, 'rb'),
                    caption='The most active repliers pie chart.')
                os.remove(pie_chart_file)

                line_chart_file = visualize_line_chart_repliers(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(line_chart_file, 'rb'),
                    caption='The most active repliers line chart.')
                os.remove(line_chart_file)

                vertical_chart_file = visualize_vertical_bar_chart_repliers(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(vertical_chart_file, 'rb'),
                    caption='The most active repliers vertical bar chart.')
                os.remove(vertical_chart_file)

                area_chart_file = visualize_area_chart_repliers(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(area_chart_file, 'rb'),
                    caption='The most active repliers area chart.')
                os.remove(area_chart_file)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'visualize_editors':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                bar_chart_file = visualize_bar_chart_editors(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(bar_chart_file, 'rb'),
                    caption='The most active editors bar chart.')
                os.remove(bar_chart_file)

                pie_chart_file = visualize_pie_chart_editors(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(pie_chart_file, 'rb'),
                    caption='The most active editors pie chart.')
                os.remove(pie_chart_file)

                line_chart_file = visualize_line_chart_editors(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(line_chart_file, 'rb'),
                    caption='The most active editors line chart.')
                os.remove(line_chart_file)

                vertical_chart_file = visualize_vertical_bar_chart_editors(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(vertical_chart_file, 'rb'),
                    caption='The most active editors vertical bar chart.')
                os.remove(vertical_chart_file)

                area_chart_file = visualize_area_chart_editors(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(area_chart_file, 'rb'),
                    caption='The most active editors area chart.')
                os.remove(area_chart_file)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'visualize_sources':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                bar_chart_file = visualize_bar_chart_sources(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(bar_chart_file, 'rb'),
                    caption='Top forward sources bar chart based on the number of messages they sent.')
                os.remove(bar_chart_file)

                pie_chart_file = visualize_pie_chart_sources(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(pie_chart_file, 'rb'),
                    caption='Proportion of messages forward sources  using a pie chart.')
                os.remove(pie_chart_file)

                area_chart_file = visualize_area_chart_sources(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(area_chart_file, 'rb'),
                    caption='Area chart ')
                os.remove(area_chart_file)

                line_chart_file = visualize_line_chart_sources(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(line_chart_file, 'rb'), )
                os.remove(line_chart_file)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'visualize_words':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                bar_chart_file = visualize_most_common_words(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(bar_chart_file, 'rb'),
                    caption='Top 10 most common words in the chat.')
                os.remove(bar_chart_file)

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")
    elif query.data == 'visualize_hours':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                bar_chart_file = visualize_bar_hours(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(bar_chart_file, 'rb'),
                    caption='Active hours bar chart.')
                os.remove(bar_chart_file)

                line_chart_file = visualize_line_hours(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(line_chart_file, 'rb'), caption='Active hours line chart.')
                os.remove(line_chart_file)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'visualize_months':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:
                months_trend_file = visualize_most_active_months_trend(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(months_trend_file, 'rb'), caption='Active months trend chart.')
                os.remove(months_trend_file)

                top_10_months_file = visualize_top_10_most_active_months(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(top_10_months_file, 'rb'), caption='Top 10 most active months.')
                os.remove(top_10_months_file)

            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'visualize_months_year':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:

                months_per_year_file = visualize_most_active_months_by_year(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(months_per_year_file, 'rb'), caption='Active months by year.')
                os.remove(months_per_year_file)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'visualize_months_all':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:

                bar_chart_file = visualize_bar_chart_months(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(bar_chart_file, 'rb'),
                    caption='Active months bar chart.')
                os.remove(bar_chart_file)

                line_chart_file = visualize_line_chart_months(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(line_chart_file, 'rb'), caption='Active months line chart.')
                os.remove(line_chart_file)

                pie_chart_file = visualize_pie_chart_months(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(pie_chart_file, 'rb'), caption='Active months pie chart.')
                os.remove(pie_chart_file)

                area_chart_file = visualize_area_chart_months(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(area_chart_file, 'rb'), caption='Active months area chart.')
                os.remove(area_chart_file)
            else:
                query.message.reply_text("Failed to process the JSON file.")
        else:
            query.message.reply_text("No JSON file found.")

    elif query.data == 'visualize_years':
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')
        file_path = context.user_data.get('file_path')
        if file_path:
            data = load_json(file_path)
            if data:

                trend_chart_year = visualize_message_trend_over_year(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(trend_chart_year, 'rb'),
                    caption='Active years bar chart.')
                os.remove(trend_chart_year)

                trend_bar_file = visualize_message_trend_over_year_bar(data)
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(trend_bar_file, 'rb'), caption='Active years bar chart.')
                os.remove(trend_bar_file)
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
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))
    dispatcher.add_handler(MessageHandler(Filters.photo, filter_photos))
    dispatcher.add_handler(MessageHandler(Filters.video, filter_videos))
    dispatcher.add_handler(MessageHandler(Filters.audio, filter_audios))
    dispatcher.add_handler(MessageHandler(Filters.voice, filter_voice))
    dispatcher.add_handler(MessageHandler(Filters.location, filter_location))
    dispatcher.add_handler(MessageHandler(Filters.contact, filter_contact))
    dispatcher.add_handler(MessageHandler(Filters.sticker, filter_sticker))
    dispatcher.add_handler(MessageHandler(Filters.poll, filter_poll))
    dispatcher.add_handler(CallbackQueryHandler(button_press))

    dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))
    dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

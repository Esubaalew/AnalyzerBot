import json
from datetime import datetime
from collections import defaultdict
from collections import Counter
import re
from typing import Any, List, Tuple


def load_json(file_path: str = 'result.json') -> Any | None:
    """
    Load JSON data from the specified file path.

    Args:
    - file_path (str): The path to the JSON file.

    Returns:
    - data (dict): The loaded JSON data.
    - None: If an error occurs during file opening or JSON parsing.
    """
    try:
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"An error occurred while loading the JSON file: {e}")
        return None


def chat_info(data: dict) -> dict:
    """
    Extract chat information from the JSON data.

    Args:
    - data (dict): The JSON data.

    Returns:
    - chat_info (dict): Dictionary containing chat information.
    """
    chat = data
    messages_count = len(data.get('messages', []))

    chat_info = {
        'name': chat.get('name', 'Unknown'),
        'type': chat.get('type', 'Unknown'),
        'id': chat.get('id', 'Unknown'),
        'messages_count': messages_count
    }

    return chat_info


def get_oldest_message(data: dict) -> dict:
    """
    Retrieves the oldest message from the JSON data.

    Args:
    - data (dict): The JSON data.

    Returns:
    - oldest_message (dict): Dictionary containing the oldest message with full timestamp.
    """

    oldest_message = {'date': '9999-12-31T23:59:59'}

    for message in data.get('messages', []):
        if 'date' in message and message['date'] < oldest_message['date']:
            oldest_message = message

    oldest_message['date'] = extract_date_info(oldest_message)

    return oldest_message


def extract_date_info(message: dict) -> dict:
    """
    Extract date information from the message and return it as a dictionary.

    Args:
    - message (dict): The message containing the date information.

    Returns:
    - date_info (dict): Dictionary containing the extracted date information.
    """
    date_str = message.get('date')
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')

    date_info = {
        'year': date_obj.year,
        'month': date_obj.month,
        'day': date_obj.day,
        'hour': date_obj.hour,
        'minute': date_obj.minute,
        'second': date_obj.second,
        'time': date_obj.strftime('%H:%M:%S')
    }

    return date_info


def get_latest_message(data: dict) -> dict:
    """
    Retrieves the latest message from the JSON data.

    Args:
    - data (dict): The JSON data.

    Returns:
    - latest_message (dict): Dictionary containing the latest message with full timestamp.
    """
    latest_message = {'date': '0000-01-01T00:00:00'}

    for message in data.get('messages', []):
        if 'date' in message and message['date'] > latest_message['date']:
            latest_message = message

    latest_message['date'] = extract_date_info(latest_message)
    return latest_message


def get_senders(data: dict) -> list:
    """
    Extracts the list of unique senders from the JSON data and ranks them by the number of messages they sent.

    Args:
    - data (dict): The JSON data.

    Returns:
    - senders_ranked (list): List of dictionaries containing sender names and the total number of messages they sent.
    """
    sender_count = defaultdict(int)

    for message in data.get('messages', []):
        sender = message.get('from')
        if sender is None:
            sender_count['Deleted Account'] += 1
        else:
            sender_count[sender] += 1

    senders_ranked = [{'sender': sender, 'messages': count} for sender, count in
                      sorted(sender_count.items(), key=lambda x: x[1], reverse=True)]
    return senders_ranked


def count_forwarded_messages(data: dict) -> int:
    """
    Count the number of forwarded messages in the provided JSON data.

    Args:
    - data (dict): The JSON data.

    Returns:
    - count (int): The number of forwarded messages.
    """
    count = 0
    for message in data.get('messages', []):
        if 'forwarded_from' in message:
            count += 1
    return count


def get_forwarded_messages(data: dict) -> list:
    """
    Extract all forwarded messages from the provided JSON data.

    Args:
    - data (dict): The JSON data.

    Returns:
    - forwarded_messages (list): List of dictionaries containing forwarded messages.
    """
    forwarded_messages = []
    for message in data.get('messages', []):
        if 'forwarded_from' in message:
            forwarded_messages.append(message)
    return forwarded_messages


def get_forwarders(data: dict) -> dict:
    """
    Get a ranking of forwarders based on the number of messages they forwarded.

    Args:
    - data (dict): The JSON data.

    Returns:
    - forwarder_ranking (dict): Dictionary containing forwarders ranked by the number of messages they forwarded.
    """
    forwarder_count = defaultdict(int)

    for message in data.get('messages', []):
        if 'forwarded_from' in message:
            forwarder = message['from']
            forwarder = forwarder if forwarder is not None else 'Deleted Account'
            forwarder_count[forwarder] += 1

    forwarder_ranking = dict(sorted(forwarder_count.items(), key=lambda x: x[1], reverse=True))
    return forwarder_ranking


def get_forward_sources(data: dict) -> dict:
    """
    Get a dictionary of users (forward sources) with the number of messages they are the source for,
    sorted from largest to smallest based on the number of messages.

    Args:
    - data (dict): The JSON data.

    Returns:
    - forward_sources_count (dict): Dictionary of users with the number of messages they are the source for,
                                    sorted from largest to smallest based on the number of messages.
    """
    forward_sources_count = defaultdict(int)

    for message in data.get('messages', []):
        if 'forwarded_from' in message:
            forward_source = message['forwarded_from']
            forward_source = forward_source if forward_source is not None else 'Deleted Account'
            forward_sources_count[forward_source] += 1

    sorted_forward_sources_count = dict(sorted(forward_sources_count.items(), key=lambda x: x[1], reverse=True))

    return sorted_forward_sources_count


def count_replies(data: dict) -> int:
    """
    Count all replies in the JSON data.

    Args:
    - data (dict): The JSON data.

    Returns:
    - reply_count (int): The total number of replies.
    """
    reply_count = 0

    for message in data.get('messages', []):
        if 'reply_to_message_id' in message:
            reply_count += 1

    return reply_count


def get_replies(data: dict) -> list:
    """
    Get a list of all messages that are replies to other messages from the JSON data.

    Args:
    - data (dict): The JSON data.

    Returns:
    - replies (list): List of all reply messages.
    """
    replies = []

    for message in data.get('messages', []):
        if 'reply_to_message_id' in message:
            replies.append(message)

    return replies


def get_repliers(data: dict) -> dict:
    """
    Get a ranking of repliers based on the number of messages they replied to.

    Args:
    - data (dict): The JSON data.

    Returns:
    - replier_ranking (dict): Dictionary containing repliers ranked by the number of messages they replied to.
    """
    replier_count = defaultdict(int)

    for message in data.get('messages', []):
        replier = message.get('from', 'Deleted Account') if message.get('from') is not None else 'Deleted Account'
        if 'reply_to_message_id' in message:
            replier_count[replier] += 1

    replier_ranking = dict(sorted(replier_count.items(), key=lambda x: x[1], reverse=True))
    return replier_ranking


def count_edited_messages(data: dict) -> int:
    """
    Count the number of edited messages in the JSON data.

    Args:
    - data (dict): The JSON data.

    Returns:
    - edited_count (int): The number of edited messages.
    """
    edited_count = 0

    for message in data.get('messages', []):
        if 'edited' in message:
            edited_count += 1

    return edited_count


def get_edited_messages(data: dict) -> list:
    """
    Get a list of all edited messages from the JSON data.

    Args:
    - data (dict): The JSON data.

    Returns:
    - edited_messages (list): List of all edited messages.
    """
    edited_messages = []

    for message in data.get('messages', []):
        if 'edited' in message:
            edited_messages.append(message)

    return edited_messages


def get_editors(data: dict) -> dict:
    """
    Get a ranking of editors based on the number of edited messages.

    Args:
    - data (dict): The JSON data.

    Returns:
    - editor_ranking (dict): Dictionary containing editors ranked by the number of edited messages.
    """
    editor_count = defaultdict(int)

    for message in data.get('messages', []):
        if 'edited' in message:
            editor = message.get('from')
            if editor is None:
                editor = 'Deleted Account'
            editor_count[editor] += 1

    editor_ranking = dict(sorted(editor_count.items(), key=lambda x: x[1], reverse=True))
    return editor_ranking


def get_longest_messages(data: dict) -> list:
    """
    Get the messages with the longest text from the JSON data

    Args:
    - data (dict): The JSON data.

    Returns:
    - longest_messages (list): List of dictionaries containing the text and sender of the messages with the longest text.
    """
    longest_messages = []
    max_length = 0

    for message in data.get('messages', []):

        text = message.get('text', '')
        length = len(text)
        if length > max_length:
            longest_messages = [{'text': text, 'sender': message.get('from', 'Unknown')}]
            max_length = length
        elif length == max_length:
            longest_messages.append({'text': text, 'sender': message.get('from', 'Unknown')})

    return longest_messages


def get_most_common_words(data: dict, top_n=10) -> list:
    """
    Get the top N most common single words in the text key of messages

    Args:
    - data (dict): The JSON data.
    - top_n (int): Number of top words to return.

    Returns:
    - most_common_words (list): List of dictionaries containing the top N most common single words along with their occurrences.
    """
    words_count = Counter()

    for message in data.get('messages', []):

        text = message.get('text', '')
        if isinstance(text, list):
            text = ' '.join(str(item) for item in text if isinstance(item, str))
        elif isinstance(text, dict):

            text = str(text)

        words = re.findall(r'\b\w+\b', text.lower())
        words_count.update(words)

    most_common_words = words_count.most_common(top_n)
    top_words_list = []
    for word, count in most_common_words:
        top_words_list.append({'word': word, 'occurrence': count})
    return top_words_list


def get_most_active_users(data: dict, top_n: int = 10) -> list:
    """
    Get the top N most active users based on the number of messages they sent, replacing None with "Deleted User".

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top users to return. Defaults to 10.

    Returns:
    - top_active_users (list): List of dictionaries containing information about the top active users.
    """
    user_message_count = defaultdict(int)

    for message in data.get('messages', []):

        sender = message.get('from')
        if sender is None:
            sender = "Deleted Account"
        user_message_count[sender] += 1

    sorted_users = sorted(user_message_count.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_active_users = [{'user': user, 'message_count': count} for user, count in sorted_users]

    return top_active_users


def get_average_message_length(data):
    total_length = 0
    total_messages = 0

    for message in data.get('messages', []):
        text = message.get('text', '')
        total_length += len(text)
        total_messages += 1

    if total_messages == 0:
        return 0

    average_length = total_length / total_messages
    return average_length


def each_average_message_length(data: dict) -> dict:
    from collections import defaultdict
    user_lengths = defaultdict(int)
    user_counts = defaultdict(int)

    for message in data.get('messages', []):
        if 'from' in message:
            message_text = message.get('text', '')
            message_length = len(message_text) if isinstance(message_text, str) else sum(
                len(part['text']) for part in message_text if isinstance(part, dict))
            user_lengths[message['from']] += message_length
            user_counts[message['from']] += 1

    average_lengths = {user: user_lengths[user] / user_counts[user] for user in user_lengths}
    return average_lengths


def get_most_active_hours(data: dict) -> list[tuple[Any, int]]:
    """
    Calculates the most active hours in the Telegram group.

    Args:
    - data (dict): The JSON data from the Telegram group export.

    Returns:
    - active_hours (Counter): A Counter object with hours as keys and message counts as values.
    """

    active_hours = Counter()

    for message in data.get('messages', []):
        message_date = datetime.fromisoformat(message['date'])
        active_hours[message_date.hour] += 1

    return active_hours.most_common()


def get_most_active_days(data: dict) -> list[tuple[Any, int]]:
    """
    Calculates the most active days in the Telegram group.

    Args:
    - data (dict): The JSON data from the Telegram group export.

    Returns:
    - active_days (Counter): A Counter object with days as keys and message counts as values.
    """

    active_days = Counter()

    for message in data.get('messages', []):
        message_date = datetime.fromisoformat(message['date'])
        active_days[message_date.strftime('%Y-%m-%d')] += 1

    return active_days.most_common()


def get_most_active_weekdays(data: dict) -> list[tuple[Any, int]]:
    """
    Calculates the most active weekdays in the Telegram group.

    Args:
    - data (dict): The JSON data from the Telegram group export.

    Returns:
    - active_weekdays (Counter): A Counter object with weekdays as keys and message counts as values.
    """

    active_weekdays = Counter()

    for message in data.get('messages', []):
        message_date = datetime.fromisoformat(message['date'])
        active_weekdays[message_date.strftime('%A')] += 1

    return active_weekdays.most_common()


def get_most_active_months(data: dict) -> list[tuple[Any, int]]:
    """
    Calculates the most active months in the Telegram group.

    Args:
    - data (dict): The JSON data from the Telegram group export.

    Returns:
    - active_months (Counter): A Counter object with months as keys and message counts as values.
    """

    active_months = Counter()

    for message in data.get('messages', []):
        message_date = datetime.fromisoformat(message['date'])
        active_months[message_date.strftime('%Y-%m')] += 1

    return active_months.most_common()


def get_user_activity(data: dict) -> dict:
    """
    Analyzes the activity of each user in the Telegram group based on different time dimensions.

    Args:
    - data (dict): The JSON data from the Telegram group export.

    Returns:
    - user_activity (dict): Dictionary containing user activity information.
    """

    user_activity = defaultdict(lambda: defaultdict(Counter))

    for message in data.get('messages', []):
        sender = message.get('from', 'Deleted Account')
        timestamp = message.get('date')
        if sender and timestamp:
            message_date = datetime.fromisoformat(timestamp)
            hour = message_date.hour
            day = message_date.strftime('%Y-%m-%d')
            weekday = message_date.strftime('%A')
            month = message_date.strftime('%Y-%m')

            user_activity[sender]['Hour'][hour] += 1
            user_activity[sender]['Day'][day] += 1
            user_activity[sender]['Weekday'][weekday] += 1
            user_activity[sender]['Month'][month] += 1

    formatted_user_activity = {}
    for user, activity_info in user_activity.items():
        formatted_activity_info = {}
        for time_dimension, counts in activity_info.items():
            most_active_info = counts.most_common(1)
            if most_active_info:
                most_active_time = most_active_info[0][0]
                most_active_count = most_active_info[0][1]
            else:
                most_active_time = 'N/A'
                most_active_count = 0
            formatted_activity_info[time_dimension] = {
                'most_active': most_active_time,
                'messages': most_active_count
            }

        overall_activity = sum(sum(counter.values()) for counter in activity_info.values())
        formatted_activity_info['Overall'] = {
            'most_active': 'N/A' if overall_activity == 0 else 'Overall',
            'messages': overall_activity
        }
        formatted_user_activity[user] = formatted_activity_info

    return formatted_user_activity


def get_most_active_year(data: dict) -> list[tuple[Any, int]]:
    """
    Calculates the most active year in the Telegram group.

    Args:
    - data (dict): The JSON data from the Telegram group export.

    Returns:
    - active_years (Counter): A Counter object with years as keys and message counts as values.
    """

    active_years = Counter()

    for message in data.get('messages', []):
        message_date = datetime.fromisoformat(message['date'])
        active_years[message_date.strftime('%Y')] += 1

    return active_years.most_common()


def get_most_active_months_all_time(data: dict) -> list:
    """
    Calculates the most active months in the Telegram group for all months and all years.

    Args:
    - data (dict): The JSON data from the Telegram group export.

    Returns:
    - active_months_list (list): A list of dictionaries with 'name' and 'messages' as keys.
    """

    active_months = Counter()
    month_names = {
        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
        '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
    }

    for message in data.get('messages', []):
        message_date = datetime.fromisoformat(message['date'])
        month_num = message_date.strftime('%m')
        active_months[month_names[month_num]] += 1

    active_months_list = [{'name': month, 'messages': count} for month, count in active_months.items()]

    return active_months_list


def get_most_active_months_by_year(data: dict) -> dict:
    """
    Calculates the most active months in the Telegram group for each year.

    Args:
    - data (dict): The JSON data from the Telegram group export.

    Returns:
    - active_months_by_year (dict): A dictionary with years as keys and a list of dictionaries
      for active months as values.
    """

    active_months_by_year = {}
    month_names = {
        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
        '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
    }

    for message in data.get('messages', []):
        message_date = datetime.fromisoformat(message['date'])
        year = message_date.strftime('%Y')
        month_num = message_date.strftime('%m')
        month_name = month_names[month_num]

        if year not in active_months_by_year:
            active_months_by_year[year] = Counter()

        active_months_by_year[year][month_name] += 1

    for year, months_counter in active_months_by_year.items():
        active_months_by_year[year] = [{'name': month, 'messages': count} for month, count in months_counter.items()]

    return active_months_by_year

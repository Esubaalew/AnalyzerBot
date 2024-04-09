import sys
import uuid

from matplotlib import pyplot as plt

from analyzer.tools import get_most_active_weekdays, chat_info


def visualize_most_active_weekdays_bar(data: dict):
    active_weekdays = get_most_active_weekdays(data)

    weekdays = [weekday for weekday, _ in active_weekdays]
    message_counts = [count for _, count in active_weekdays]

    plt.figure(figsize=(10, 6))
    plt.bar(weekdays, message_counts, color='skyblue')
    plt.xlabel('Weekday')
    plt.ylabel('Message Count')
    plt.title(f'Most Active Weekdays in the {chat_info(data)["name"]}')
    plt.xticks(rotation=45)
    plt.tight_layout()

    file_name = f"bar_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name


def visualize_most_active_weekdays_pie(data: dict):
    active_weekdays = get_most_active_weekdays(data)

    weekdays = [weekday for weekday, _ in active_weekdays]
    message_counts = [count for _, count in active_weekdays]

    plt.figure(figsize=(8, 8))
    plt.pie(message_counts, labels=weekdays, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title(f'Most Active Weekdays in the {chat_info(data)["name"]}')

    file_name = f"bar_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name

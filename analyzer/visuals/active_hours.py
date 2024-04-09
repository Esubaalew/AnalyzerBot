import uuid
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from analyzer.tools import get_most_active_hours, chat_info


def visualize_bar_hours(data: dict):
    active_hours = get_most_active_hours(data)
    hours, counts = zip(*active_hours)

    ethiopian_hours = [(datetime.strptime(str(hour), '%H') + timedelta(hours=3)).strftime('%I %p') for hour in hours]

    colors = ['skyblue', 'orange', 'green', 'red', 'purple', 'yellow', 'brown', 'pink', 'gray', 'cyan', 'magenta',
              'lightgreen']

    plt.figure(figsize=(12, 6))
    plt.bar(ethiopian_hours, counts, color=colors)
    plt.xlabel('Hour of the Day (Ethiopian Time)')
    plt.ylabel('Message Count')
    plt.title(f'Most Active Hours in the {chat_info(data)["name"]}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    file_name = f"bar_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)
    plt.close()

    return file_name


def visualize_line_hours(data: dict):
    active_hours = get_most_active_hours(data)
    hours, counts = zip(*active_hours)

    ethiopian_hours = [(datetime.strptime(str(hour), '%H') + timedelta(hours=3)).strftime('%I %p') for hour in hours]

    plt.figure(figsize=(14, 6))
    plt.plot(ethiopian_hours, counts, marker='o', color='skyblue', linestyle='-')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Message Count')
    plt.title(f'Most Active Hours in the {chat_info(data)["name"]}')
    plt.xticks(range(24))
    plt.grid(True, linestyle='--', alpha=0.7)
    file_name = f"line_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)
    plt.close()

    return file_name

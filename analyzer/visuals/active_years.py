import uuid

from matplotlib import pyplot as plt

from analyzer.tools import get_most_active_year, chat_info


def visualize_message_trend_over_year(data: dict):
    """
    Visualize the change in message activity over time using a line plot.

    Args:
    - data (dict): The JSON data from the Telegram group export.
    """
    active_years_data = get_most_active_year(data)

    sorted_years = active_years_data
    years, message_counts = zip(*sorted_years)

    plt.figure(figsize=(10, 5))
    plt.plot(years, message_counts, marker='o')
    plt.title(f'Number of Messages Over Time for {chat_info(data)["name"]}')
    plt.xlabel('Year')
    plt.ylabel('Number of Messages')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    file_name = f"tre_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name


def visualize_message_trend_over_year_bar(data: dict):
    """
    Visualize the change in message activity over time using a bar chart.

    Args:
    - data (dict): The JSON data from the Telegram group export.
    """
    active_years_data = get_most_active_year(data)

    sorted_years = active_years_data
    years, message_counts = zip(*sorted_years)

    plt.figure(figsize=(10, 5))
    plt.bar(years, message_counts, color='skyblue')
    plt.title(f'Number of Messages Over Years for {chat_info(data)["name"]}')
    plt.xlabel('Year')
    plt.ylabel('Number of Messages')
    plt.xticks(rotation=45)
    plt.tight_layout()
    file_name = f"bar_trend_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name

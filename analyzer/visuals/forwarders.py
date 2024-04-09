import uuid

from matplotlib import pyplot as plt

import seaborn as sns

from analyzer.tools import get_forwarders, chat_info


def visualize_forwarders_bar_chart(data: dict, top_n: int = 10):
    """
    Visualize the top N forwarders based on the number of messages they forwarded.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top forwarders to visualize. Defaults to 10.
    """

    # Get forwarders data
    forwarder_ranking = get_forwarders(data)
    top_forwarders = list(forwarder_ranking.keys())[:top_n]
    message_counts = list(forwarder_ranking.values())[:top_n]

    # Create bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x=message_counts, y=top_forwarders, palette="viridis")
    plt.xlabel('Message Count')
    plt.ylabel('Forwarder')
    plt.title(f'Top {top_n} Forwarders by Message Count for {chat_info(data)["name"]}')
    file_name = f"bar_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name


def visualize_forwarders_pie_chart(data: dict, top_n: int = 6):
    """
    Visualize the proportion of messages forwarded by each forwarder using a pie chart.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top forwarders to include. Defaults to 10.
    """
    forwarder_ranking = get_forwarders(data)
    top_forwarders = list(forwarder_ranking.keys())[:top_n]
    message_counts = list(forwarder_ranking.values())[:top_n]

    plt.figure(figsize=(8, 8))
    plt.pie(message_counts, labels=top_forwarders, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
    plt.title(f'Proportion of Messages Forwarded by Top {top_n} Forwarders for {chat_info(data)["name"]}')
    plt.axis('equal')
    file_name = f"bar_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name


def visualize_forwarders_vertical_bar_chart(data: dict, top_n: int = 10):
    """
    Visualize the top N forwarders based on the number of messages they forwarded.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top forwarders to visualize. Defaults to 10.
    """

    forwarder_ranking = get_forwarders(data)
    top_forwarders = list(forwarder_ranking.keys())[:top_n]
    message_counts = list(forwarder_ranking.values())[:top_n]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_forwarders, y=message_counts, palette="viridis")
    plt.xlabel('Forwarder')
    plt.ylabel('Message Count')
    plt.title(f'Top {top_n} Forwarders by Message Count for {chat_info(data)["name"]}')
    file_name = f"bar_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name


def visualize_forwarders_line_chart(data: dict, top_n: int = 10):
    """
    Visualize the top N forwarders based on the number of messages they forwarded using a line chart.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top forwarders to visualize. Defaults to 10.
    """

    forwarder_ranking = get_forwarders(data)
    top_forwarders = list(forwarder_ranking.keys())[:top_n]
    message_counts = list(forwarder_ranking.values())[:top_n]

    plt.figure(figsize=(10, 6))
    plt.plot(top_forwarders, message_counts, marker='o', color='skyblue', linestyle='-')
    plt.xlabel('Forwarder')
    plt.ylabel('Message Count')
    plt.title(f'Top {top_n} Forwarders (Line Chart) for {chat_info(data)["name"]}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True)
    file_name = f"bar_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name


def visualize_forwarders_area_chart(data: dict, top_n: int = 10):
    """
    Visualize the top N forwarders based on the number of messages they forwarded using an area chart.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top forwarders to visualize. Defaults to 10.
    """

    forwarder_ranking = get_forwarders(data)
    top_forwarders = list(forwarder_ranking.keys())[:top_n]
    message_counts = list(forwarder_ranking.values())[:top_n]

    plt.figure(figsize=(10, 6))
    plt.fill_between(top_forwarders, message_counts, color='skyblue', alpha=0.4)
    plt.plot(top_forwarders, message_counts, color='skyblue', alpha=0.8, marker='o', linestyle='-')
    plt.xlabel('Forwarder')
    plt.ylabel('Message Count')
    plt.title(f'Top {top_n} Forwarders (Area Chart) for {chat_info(data)["name"]}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True)
    file_name = f"bar_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name

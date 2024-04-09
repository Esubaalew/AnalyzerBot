import uuid

from matplotlib import pyplot as plt
import seaborn as sns

from analyzer.tools import get_repliers, chat_info


def visualize_bar_chart_repliers(data: dict, top_n: int = 10):
    """
    Visualize the top N repliers based on the number of messages they replied to.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top repliers to visualize. Defaults to 10.
    """

    # Get repliers data
    replier_ranking = get_repliers(data)
    top_repliers = list(replier_ranking.keys())[:top_n]
    message_counts = list(replier_ranking.values())[:top_n]

    # Create bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x=message_counts, y=top_repliers, palette="viridis")
    plt.xlabel('Message Count')
    plt.ylabel('Replier')
    plt.title(f'Top {top_n} Repliers by Message Count for {chat_info(data)["name"]}')
    file_name = f"bar_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name


def visualize_pie_chart_repliers(data: dict, top_n: int = 6):
    """
    Visualize the proportion of messages replied to by each replier using a pie chart.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top repliers to include. Defaults to 10.
    """
    replier_ranking = get_repliers(data)
    top_repliers = list(replier_ranking.keys())[:top_n]
    message_counts = list(replier_ranking.values())[:top_n]

    plt.figure(figsize=(8, 8))
    plt.pie(message_counts, labels=top_repliers, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
    plt.title(f'Proportion of Messages Replied to by Top {top_n} Repliers for {chat_info(data)["name"]}')
    plt.axis('equal')
    file_name = f"pie_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name


def visualize_vertical_bar_chart_repliers(data: dict, top_n: int = 10):
    """
    Visualize the top N repliers based on the number of messages they replied to.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top repliers to visualize. Defaults to 10.
    """

    replier_ranking = get_repliers(data)
    top_repliers = list(replier_ranking.keys())[:top_n]
    message_counts = list(replier_ranking.values())[:top_n]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_repliers, y=message_counts, palette="viridis")
    plt.xlabel('Replier')
    plt.ylabel('Message Count')
    plt.title(f'Top {top_n} Repliers by Message Count for {chat_info(data)["name"]}')
    file_name = f"vertical_bar_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name


def visualize_line_chart_repliers(data: dict, top_n: int = 10):
    """
    Visualize the top N repliers based on the number of messages they replied to using a line chart.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top repliers to visualize. Defaults to 10.
    """

    replier_ranking = get_repliers(data)
    top_repliers = list(replier_ranking.keys())[:top_n]
    message_counts = list(replier_ranking.values())[:top_n]

    plt.figure(figsize=(10, 6))
    plt.plot(top_repliers, message_counts, marker='o', color='skyblue', linestyle='-')
    plt.xlabel('Replier')
    plt.ylabel('Message Count')
    plt.title(f'Top {top_n} Repliers (Line Chart) for {chat_info(data)["name"]}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True)
    file_name = f"line_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name


def visualize_area_chart_repliers(data: dict, top_n: int = 10):
    """
    Visualize the top N repliers based on the number of messages they replied to using an area chart.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top repliers to visualize. Defaults to 10.
    """

    replier_ranking = get_repliers(data)
    top_repliers = list(replier_ranking.keys())[:top_n]
    message_counts = list(replier_ranking.values())[:top_n]

    plt.figure(figsize=(10, 6))
    plt.fill_between(top_repliers, message_counts, color='skyblue', alpha=0.4)
    plt.plot(top_repliers, message_counts, color='skyblue', alpha=0.8, marker='o', linestyle='-')
    plt.xlabel('Replier')
    plt.ylabel('Message Count')
    plt.title(f'Top {top_n} Repliers (Area Chart) for {chat_info(data)["name"]}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True)
    file_name = f"area_bar_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name

import uuid

from matplotlib import pyplot as plt
import seaborn as sns

from analyzer.tools import get_editors, chat_info


def visualize_bar_chart_editors(data: dict, top_n: int = 10):
    """
    Visualize the top N editors based on the number of edited messages.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top editors to visualize. Defaults to 10.
    """

    # Get editors data
    editor_ranking = get_editors(data)
    top_editors = list(editor_ranking.keys())[:top_n]
    edited_message_counts = list(editor_ranking.values())[:top_n]

    # Create bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x=edited_message_counts, y=top_editors, palette="viridis")
    plt.xlabel('Edited Message Count')
    plt.ylabel('Editor')
    plt.title(f'Top {top_n} Editors by Edited Message Count for {chat_info(data)["name"]}')
    file_name = f"bar_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return  file_name


def visualize_pie_chart_editors(data: dict, top_n: int = 6):
    """
    Visualize the proportion of edited messages by each editor using a pie chart.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top editors to include. Defaults to 6.
    """
    editor_ranking = get_editors(data)
    top_editors = list(editor_ranking.keys())[:top_n]
    edited_message_counts = list(editor_ranking.values())[:top_n]

    plt.figure(figsize=(8, 8))
    plt.pie(edited_message_counts, labels=top_editors, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
    plt.title(f'Proportion of Edited Messages by Top {top_n} Editors for {chat_info(data)["name"]}')
    plt.axis('equal')
    file_name = f"pie_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()
    return  file_name


def visualize_vertical_bar_chart_editors(data: dict, top_n: int = 10):
    """
    Visualize the top N editors based on the number of edited messages.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top editors to visualize. Defaults to 10.
    """

    editor_ranking = get_editors(data)
    top_editors = list(editor_ranking.keys())[:top_n]
    edited_message_counts = list(editor_ranking.values())[:top_n]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_editors, y=edited_message_counts, palette="viridis")
    plt.xlabel('Editor')
    plt.ylabel('Edited Message Count')
    plt.title(f'Top {top_n} Editors by Edited Message Count for {chat_info(data)["name"]}')
    file_name = f"vertical_bar_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return  file_name

def visualize_line_chart_editors(data: dict, top_n: int = 10):
    """
    Visualize the top N editors based on the number of edited messages using a line chart.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top editors to visualize. Defaults to 10.
    """

    editor_ranking = get_editors(data)
    top_editors = list(editor_ranking.keys())[:top_n]
    edited_message_counts = list(editor_ranking.values())[:top_n]

    plt.figure(figsize=(10, 6))
    plt.plot(top_editors, edited_message_counts, marker='o', color='skyblue', linestyle='-')
    plt.xlabel('Editor')
    plt.ylabel('Edited Message Count')
    plt.title(f'Top {top_n} Editors (Line Chart) for {chat_info(data)["name"]}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True)
    file_name = f"line_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return  file_name


def visualize_area_chart_editors(data: dict, top_n: int = 10):
    """
    Visualize the top N editors based on the number of edited messages using an area chart.

    Args:
    - data (dict): The JSON data.
    - top_n (int): The number of top editors to visualize. Defaults to 10.
    """

    editor_ranking = get_editors(data)
    top_editors = list(editor_ranking.keys())[:top_n]
    edited_message_counts = list(editor_ranking.values())[:top_n]

    plt.figure(figsize=(10, 6))
    plt.fill_between(top_editors, edited_message_counts, color='skyblue', alpha=0.4)
    plt.plot(top_editors, edited_message_counts, color='skyblue', alpha=0.8, marker='o', linestyle='-')
    plt.xlabel('Editor')
    plt.ylabel('Edited Message Count')
    plt.title(f'Top {top_n} Editors (Area Chart) for {chat_info(data)["name"]}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True)
    file_name = f"area_chart_{uuid.uuid4()}.png"

    plt.savefig(file_name)

    plt.close()

    return file_name


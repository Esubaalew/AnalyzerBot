import uuid

from matplotlib import pyplot as plt
import seaborn as sns

from analyzer.tools import get_most_common_words, chat_info


def visualize_most_common_words(data: dict, top_n: int = 10):
    """
    Visualize the top N most common single words in the text key of messages using a bar chart.

    Args:
    - data (dict): The JSON data.
    - top_n (int): Number of top words to visualize. Defaults to 10.
    """
    top_words = get_most_common_words(data, top_n)
    words = [word['word'] for word in top_words]
    occurrences = [word['occurrence'] for word in top_words]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=occurrences, y=words, palette="viridis")
    plt.xlabel('Occurrences')
    plt.ylabel('Word')
    plt.title(f'Top {top_n} Most Common Words for {chat_info(data)["name"]}')
    file_name = f"chart_{uuid.uuid4()}.png"
    plt.savefig(file_name)
    plt.close()
    return file_name

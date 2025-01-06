# AnalyzerBot

AnalyzerBot is a Telegram chat analysis bot designed to process and visualize data from exported Telegram chat JSON files. With its intuitive setup and modular design, AnalyzerBot helps users uncover insights and trends from their Telegram conversations.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Demo](#demo)

## Features

- **Chat Analysis**: Process exported Telegram chat JSON files for detailed analysis.
- **Data Visualization**: Generate insightful visuals to better understand chat patterns and trends.
- **Extensibility**: Modular design allows for easy integration of additional analysis tools.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Esubaalew/AnalyzerBot.git
   cd AnalyzerBot-main
   ```

2. Set up a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Export your Telegram chat history in JSON format using the Telegram app.
2. Place the exported JSON file in the appropriate directory.
3. Run the bot:

   ```bash
   python bot.py
   ```

4. Follow the on-screen instructions to analyze your chat data and view visualizations.

## Project Structure

```
AnalyzerBot-main/
├── .gitignore
├── bot.py               # Main script to run the bot
├── requirements.txt     # Python dependencies
├── analyzer/            # Core analysis module
│   ├── __init__.py
│   ├── tools.py         # Utility functions for analysis
│   └── visuals/         # Visualization scripts and assets
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch.
4. Open a pull request describing your changes.


## Demo

Try out AnalyzerBot directly on Telegram: [LiyuBot](https://t.me/liyurobot)

# AI-Powered Telegram Chatbot

This project is an AI-powered Telegram chatbot built using Python. It integrates with OpenAI's GPT-4 to provide intelligent and context-aware conversations. The bot is designed to assist users by answering queries, providing information, and engaging in meaningful dialogue.

## Features

- **AI-Driven Conversations**: Leverages OpenAI's GPT-4 model for generating human-like responses.
- **Conversation Memory**: Maintains a history of interactions with each user, allowing for contextually relevant responses.
- **Environment Variable-based Configuration**: Ensures security by handling API keys and sensitive data through environment variables.
- **Error Handling**: Gracefully manages errors and API rate limits.

## Project Structure

- `bot.py`: The main Python script that handles the bot's logic, integrating with Telegram's API and OpenAI's GPT-4 model.
- `config.py`: (Optional) A configuration file for storing API keys and tokens.
- `requirements.txt`: Contains a list of Python packages required for the project.

## How to Use

### Prerequisites

- Python 3.8 or higher.
- Telegram account and a bot token from BotFather.
- OpenAI API key.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/mvishiu11/CustomerServiceBot.git
```

2. Navigate to the project directory:

```bash
cd CustomerServiceBot
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```


### Configuration

1. You can use `config.py` to set your API token variables, as this project does by default. Remember not to upload this file to public repositories for security reasons.

2. Set your OpenAI API key and Telegram bot token as environment variables:
- Linux/macOS:
  ```
  export OPENAI_API_KEY='your_api_key_here'
  export TELEGRAM_BOT_TOKEN='your_bot_token_here'
  ```
- Windows (Command Prompt):
  ```
  set OPENAI_API_KEY=your_api_key_here
  set TELEGRAM_BOT_TOKEN=your_bot_token_here
  ```

### Running the Bot

Execute the `bot.py` script to start the bot:

```bash
python bot.py
```


Your bot should now be live on Telegram and ready to interact with users.

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License - see the [license file](LICENSE) for details.

## Contact

For any queries or further assistance, please contact [Jakub Muszyński](mailto:jakub.m.muszynski@gmail.com).

---

*README created by [Jakub Muszyński](https://github.com/mvishiu11)*

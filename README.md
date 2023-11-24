# ktlschatgpt

Looking for a game-changing solution that's both powerful and free? Look no further! ktlschatgpt is your all-in-one, completely free Telegram bot, equipped with a seamlessly integrated chatGPT for all your business and personal needs.
Just deploy it to your server and use it for your purposes.

## Deployment

1. Clone this repository to your local machine with:

   ```bash
   git clone https://github.com/Shulcz/ktlschatgpt.git
   ```

2. Navigate to the Repository Directory:

   ```bash
   cd ktlschatgpt
   ```

3. Set up a Virtual Environment (Optional but Recommended):
   ```sh
   python -m venv venv
   ```

- Activate the virtual environment:
  - **On macOS and Linux:**
  ```sh
  source venv/bin/activate
  ```

5. Install Required Packages:

   ```sh
   pip install -r requirements.txt

   ```

6. Create a `.env` file and specify the required environment variables:

   ```env
   BOT_TOKEN=<bot_token>
   WHITELIST_USERS=user_id_1,user_id_2,user_id_3
   ```

7. Run the Application:
   ```sh
   python app.py
   ```

## Periodic Updates

To update the bot, use the provided `g4f_update` script:

```bash
sh g4f_update.sh
```

## Usage

### Chat History Clearing

To clear the chat history with the bot, send the /newchat command.

### Chat History Database

All interactions with the bot are logged in the chat_history.db database, which is created after the bot is initialized.

### User Whitelisting

Specify user IDs in the .env file to create a whitelist of users who can access the bot:

```env
WHITELIST_USERS=user_id_1,user_id_2,user_id_3
```

## Contributing

Feel free to contribute to the development of this bot by creating issues or submitting pull requests.

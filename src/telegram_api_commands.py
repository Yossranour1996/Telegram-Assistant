from query_chatgpt import generate_system_prompt, bot_query_chatgpt_api
from telegram.ext import ContextTypes
from telegram import Update
import numpy as np
import logging

from telegram_api_helpers import (
    BotConfig,
    BotMessages,
    chunk_response,
    write_response_to_text_file
)


def handle_response(text: str) -> str:
    """
    Respond to general messages.
    """
    lower_case_text: str = text.lower()

    if "hello" in lower_case_text:
        return "Hello!"

    if "help" in lower_case_text:
        return BotMessages.helper_message

    return np.random.choice([
        BotMessages.random_response_1,
        BotMessages.random_response_2,
        BotMessages.random_response_3,
        BotMessages.random_response_4
    ])


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(BotMessages.start_message, parse_mode=BotConfig.PARSE_MODE)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Type /learn followed by a topic to learn Georgian. For example: /learn greetings.", parse_mode=BotConfig.PARSE_MODE)


async def learn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract topic from user command
    topic = ' '.join(context.args)
    if not topic:
        await update.message.reply_text(BotMessages.topic_not_provided_error, parse_mode=BotConfig.PARSE_MODE)
        return

    # Query ChatGPT for the specific topic
    response = bot_query_chatgpt_api(topic)
    await update.message.reply_text(response, parse_mode=BotConfig.PARSE_MODE)


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Coming soon...", parse_mode=BotConfig.PARSE_MODE)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")


async def test_google_map_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://goo.gl/maps/4GRcDoxK1jP1KyrN6"
    msg = f"Here is a link to Google Maps: {url}"
    await update.message.reply_text(msg, parse_mode=BotConfig.PARSE_MODE)


async def test_debug_message_format_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open('test-response.txt', 'r') as f:
        fake_message = f.read()
    await update.message.reply_text(fake_message, parse_mode=BotConfig.PARSE_MODE)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_username: str):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    user: str = update.message.chat.username
    user_id: int = update.message.chat.id

    logging.info(f"Received message from user {user_id} ({user}): {text}")

    if message_type == 'group' and bot_username in text:
        new_text: str = text.replace(bot_username, "").strip()
        response = handle_response(new_text)
    else:
        response = handle_response(text)

    logging.info(f"Sending response to user {user_id} ({user}): {response}")
    await update.message.reply_text(response, parse_mode=BotConfig.PARSE_MODE)

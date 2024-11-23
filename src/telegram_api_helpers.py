
from query_chatgpt import  generate_system_prompt,query_chatgpt_api
import telegramify_markdown
from pprint import pprint
import numpy as np
import requests
import logging
import re


class BotConfig:
    PARSE_MODE = 'MarkdownV2'
    SPECIAL_CHARS = ['\\', '_', '*', '[', ']', '(', ')', '~', '`', '>', '<', '&', '#', '+', '-', '=', '|', '{', '}', '.', '!']

class BotMessages:
    LEARN_KEY = '/learn'
    helper_message = (
        "Available commands:\n"
        "- /learn [topic]: Get general language tips on any topic.\n"
        "- /diseases [topic]: Get disease-related vocabulary and explanations.\n"
        "- /anatomy [topic]: Learn anatomy vocabulary.\n"
        "- /pharma [topic]: Explore pharmacology terms.\n"
        "- /symptoms [topic]: Understand common symptom terminology."
    )    
    anatomy_error = "Please provide a topic after /anatomy. For example: '/anatomy heart'."
    pharma_error = "Please provide a topic after /pharma. For example: '/pharma antibiotics'."
    symptoms_error = "Please provide a topic after /symptoms. For example: '/symptoms fever'."
    diseases_error = "Please provide a topic after /diseases. For example: '/diseases diabetes'."
    topic_not_provided_error = f"Please provide a topic after {LEARN_KEY}. For example: '{LEARN_KEY} greetings'."
    about_message = """
        *Georgian Language Bot*

        GeorgianLanguageBot is designed to assist users in learning Georgian, with a focus on medical vocabulary and terminology for healthcare students."""
    start_message = (
        "Welcome to GeorgianLanguageBot! I'm here to help you learn Georgian.\n"
        "Type /help to see available commands and get started."
    )
    random_response_1 = "I'm not sure what you're asking. Try typing /help."
    random_response_2 = "Oops, I didn’t understand that. Type /help for assistance."
    random_response_3 = "I’m here to help you with Georgian language basics. Type /help to learn more."
    random_response_4 = "Hmmm, I couldn’t quite understand. Type /help for guidance."

    @staticmethod
    def sample_random_response():
        return np.random.choice([BotMessages.random_response_1, BotMessages.random_response_2, BotMessages.random_response_3, BotMessages.random_response_4])


class event_instance:
    """
    Extract event instance from the Telegram API response.
    """
    def __init__(self, event):
        self.update_id = event['update_id']
        self.message_id = event['message']['message_id']
        self.from_id = event['message']['from']['id']
        self.is_bot = event['message']['from'].get('is_bot', False)
        self.first_name = event['message']['from'].get('first_name', '')
        self.last_name = event['message']['from'].get('last_name', '')
        self.language_code = event['message']['from'].get('language_code', '')
        self.chat_id = event['message']['chat']['id']
        self.chat_first_name = event['message']['chat'].get('first_name', '')
        self.chat_last_name = event['message']['chat'].get('last_name', '')
        self.chat_type = event['message']['chat'].get('type', '')
        self.date = event['message']['date']
        self.text = event['message'].get('text', '')


def split_message(content: str) -> list:
    """
    Split message into chunks that are less than the Telegram API limit.
    """
    # sections = re.split(r'\n#+\s', content)
    sections = re.split(r'\n#+\s', content)

    sections = [section.strip() for section in sections]
    return sections


def escape_special_chars(text: str, SPECIAL_CHARS=BotConfig.SPECIAL_CHARS) -> str:
    for char in SPECIAL_CHARS:
        text = text.replace(char, f'\\{char}')
    return text


def chunk_response(text_response: str):
    logging.info('Sending response in chunks...')
    for _i, _message in enumerate(split_message(text_response)):
        # remove '###' from headings and '*'
        # _msg = re.sub(r'\n#+\s', '\n ', _message)
        # _msg = re.sub(r'\n\*\s', '\n ', _msg)
        # _msg = escape_special_chars(_message, BotConfig.SPECIAL_CHARS)
        _msg = _message

        yield _i, _msg


def write_response_to_text_file(text_response: str, filename: str = 'response.txt'):
    with open(filename, 'w') as f:
        f.write(text_response)

def send_message(chat_id, text, BOT_API_TOKEN):
    url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"

    # Ensure text encoding is UTF-8 compliant
    text = telegramify_markdown.markdownify(
        text,
        max_line_length=None,
        normalize_whitespace=False
    ).encode('utf-8', 'ignore').decode('utf-8')  # Encode and decode as UTF-8 to handle special characters

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": BotConfig.PARSE_MODE
    }
    logging.info(f"Sending message (chat_id:{chat_id}) : payload : {payload}")
    response = requests.post(url, json=payload)
    return response.json()


def bot_query_chatgpt_api(text: str) -> str:
    # Remove the command part (`/learn`) from the text to get the topic
    topic = text.replace(BotMessages.LEARN_KEY, '').strip()

    # Check if a topic was provided; if not, return an error message
    if not topic:
        return BotMessages.topic_not_provided_error

    # Generate the system prompt based on the topic
    prompt = generate_system_prompt(topic)
    logging.info(f"Generated system prompt for topic '{topic}': {prompt}")

    # Query ChatGPT-4 with the generated prompt
    response = query_chatgpt_api(prompt)
    
    return response

class BotCommands:
    message_handler_map = {
        '/start': BotMessages.start_message,
        '/help': BotMessages.helper_message,
        '/about': BotMessages.about_message,
        # BotMessages.LEARN_KEY: bot_query_chatgpt_api, 
        # New function to query ChatGPT-4
        # '/learn': bot_query_chatgpt_api       
        '/anatomy': lambda: bot_query_chatgpt_api(generate_system_prompt("anatomy")),
        '/pharma': lambda: bot_query_chatgpt_api(generate_system_prompt("pharmacology")),
        '/symptoms': lambda: bot_query_chatgpt_api(generate_system_prompt("symptoms")),
        '/diseases': lambda: bot_query_chatgpt_api(generate_system_prompt("diseases")),  # Directly map '/learn' to the function
        '/learn': bot_query_chatgpt_api,  # Ensure this function exists and is correctly set up

    }

def handle_message(chat_id, text, BOT_API_TOKEN):
    # Extract the command keyword (first word)
    command, *args = text.strip().split(' ')
    command = command.lower()
    topic = ' '.join(args).strip()

    # Define a dictionary to map commands to error messages for missing topics
    topic_required_commands = {
        '/anatomy': BotMessages.anatomy_error,
        '/pharma': BotMessages.pharma_error,
        '/symptoms': BotMessages.symptoms_error,
        '/diseases': BotMessages.diseases_error,
    }

    # Check if the command is in the list of commands requiring a topic
    if command in topic_required_commands:
        # If topic is missing, send the appropriate error message
        if not topic:
            send_message(chat_id, topic_required_commands[command], BOT_API_TOKEN)
            return True
        
        # If topic is provided, generate the response for the specific command
        response_message = bot_query_chatgpt_api(f"{command} {topic}")

    elif command == BotMessages.LEARN_KEY:
        # Handle `/learn <topic>` as before
        if not topic:
            send_message(chat_id, BotMessages.topic_not_provided_error, BOT_API_TOKEN)
            return True
        response_message = bot_query_chatgpt_api(f"{BotMessages.LEARN_KEY} {topic}")

    elif command in BotCommands.message_handler_map:
        # Handle other commands as before
        response = BotCommands.message_handler_map[command]
        response_message = response() if callable(response) else response

    else:
        # Fallback to random response if command is unrecognized
        response_message = BotMessages.sample_random_response()

    # Send the response message in chunks if needed
    for _, msg_chunk in chunk_response(response_message):
        send_message(chat_id, msg_chunk, BOT_API_TOKEN)

    return True
from dotenv import load_dotenv
import logging
import json
import os
from telegram_api_helpers import event_instance, handle_message

# Load environment variables
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
load_dotenv()
BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
OPENAI_API_TOKEN = os.getenv("OPENAI_API_TOKEN")

def lambda_handler(event, context):
    try:
        logging.info("Processing incoming event...")
        logging.info(f"Event: {event}")
        logging.info(f"Context: {context}")

        # Parse the event body as JSON
        body = event.get('body')
        if not body:
            logging.error("No body in event")
            return {"statusCode": 400, "body": "No body in request"}

        # Create an event instance from the JSON body
        new_event = event_instance(json.loads(body))
        logging.info(f"Received message from user {new_event.first_name} {new_event.last_name} ({new_event.from_id}): {new_event.text}")

        # Process the message if text exists
        if new_event.text:
            response_message = handle_message(new_event.chat_id, new_event.text, BOT_API_TOKEN)
            logging.info(f"Response message: {response_message}")

        # Send a success response back to Telegram
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "Message processed successfully"})
        }

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An error occurred"})
        }

# from dotenv import load_dotenv
# import logging
# import json
# import os

# from telegram_api_helpers import (event_instance, handle_message)


# # load env --------------------------------------------------------------------------------------------->>
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# load_dotenv()
# BOT_API_TOKEN: str = os.getenv("BOT_API_TOKEN")
# BOT_USERNAME: str = os.getenv("BOT_USERNAME")
# OPENAI_API_TOKEN: str = os.getenv("OPENAI_API_TOKEN")

# def lambda_handler(event, context):
#     try:
        
#         print('Processing event...')
#         print(f'Event:   {event}')
#         print(f'Context: {context}')
#         new_event = event_instance(json.loads(event['body']))
#         logging.info(f"Received message from use {new_event.first_name} {new_event.last_name} ({new_event.from_id}) : {new_event.text}.")


#         if new_event.text:
#             handle_message(new_event.chat_id, new_event.text, BOT_API_TOKEN)

#         print('Response sent.')
#         return {
#             'statusCode': 200,
#             'body': 'Success'
#         }
#     except Exception as e:
#         logging.error(f'An error occurred: {str(e)}')
#         logging.error(f'Event: {event}')
#         logging.error(f'Context: {context}')
#         return {
#             'statusCode': 500,
#             'body': 'Error'
#         }



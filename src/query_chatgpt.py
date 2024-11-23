
import google.generativeai as genai
from urllib.parse import quote
import re
import os
from openai import OpenAI
from dotenv import load_dotenv
import logging

load_dotenv() 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_system_prompt(topic: str) -> str:
    # Dictionary for topic-specific prompts
    prompts = {
        "learn": f"""
            You are a Georgian language tutor providing general language insights.

            - The topic is: {topic}.
            - Provide relevant information in English, common phrases in Georgian with pronunciation guidance, and cultural insights.
            - Structure sections as:
                - Overview of the topic in simple terms.
                - provide the Georgian text and Key phrases in Georgian with pronunciation.
                - Any relevant Georgian cultural context related to the topic.
                - IMPORTANT: Limit explanations to 200 characters.

            """,
        "anatomy": """
            You are a Georgian language tutor focused on medical anatomy terms.

            - Provide an overview of essential anatomy vocabulary.
            - provide the Georgian text  and Include key Georgian terms for organs and body parts with phonetic pronunciation.
            - IMPORTANT: Limit explanations to 200 characters.
            """,
        "pharmacology": """
            You are a Georgian language assistant with knowledge in pharmacology.

            - Provide an introduction to common pharmacology terms, including medications, their uses, and common side effects.
            - provide the Georgian text  and Include Georgian translations and pronunciation for each term.
            - IMPORTANT: Limit explanations to 200 characters.

            """,
        "diseases": """
            You are a Georgian language assistant specializing in medical terminology for diseases.

            - Provide vocabulary and phrases related to common diseases, symptoms, and diagnoses.
            - provide the Georgian text  and Offer Georgian translations and pronunciation for terms.
            - Limit responses to essential, concise phrases for medical discussions.
            - IMPORTANT: Limit explanations to 200 characters.

            """,
        "symptoms": """
            You are a Georgian language assistant focused on terminology for symptoms.

            - Provide terms and phrases used to describe common symptoms.
            - provide the Georgian text  and Include Georgian translations, pronunciation, and any cultural context.
            - IMPORTANT: Limit explanations to 200 characters.

            """,
    }

    # Choose prompt based on topic, falling back to a general prompt if the topic is not specified
    return prompts.get(topic, prompts["learn"])

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_chatgpt_api(prompt: str, model="gpt-4"):
    try:
        # Log the generated prompt
        logging.info(f"Generated prompt: {prompt}")

        # Create the chat completion request
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful Georgian language tutor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5,
            top_p=0.8
        )

        # Access the response content directly
        result = completion.choices[0].message.content
        logging.info(f"OpenAI API response: {result}")  # Log response in UTF-8
        return result
    except Exception as e:
        logging.error(f"Error querying ChatGPT-4 API: {e}")
        return "Sorry, I’m having trouble generating a response right now."

# def generate_system_prompt(topic: str) -> str:
#     medical_topics = {
#         "anatomy": "Key terms and phrases related to the human body and its parts.",
#         "pharmacology": "Basic vocabulary about medications, their uses, and side effects.",
#         "diseases": "Common terms for diseases, symptoms, and diagnosis.",
#         "symptoms": "Phrases and vocabulary related to symptoms and patient communication."
#     }

#     if topic in medical_topics:
#         return f"""
#         You are a Georgian language assistant with a focus on medical terminology.

#         - The topic is: {topic}.
#         - Include terms and phrases commonly used in {medical_topics[topic]}.
#         - Limit the response to 300 characters.
#         - Provide translations, Georgian script, and pronunciation where relevant.
#         - Include examples in medical context when possible.
#         """
#     else:
#         return f"""
#         You are a Georgian language tutor and cultural guide.

#         - The topic is: {topic}.
#         - Provide general language insights and useful phrases.
#         - Limit the response to 300 characters.
#         """



# # Initialize the OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def query_chatgpt_api(topic: str, model="gpt-4"):
#     try:
#         # Generate a detailed system prompt based on the topic
#         prompt = generate_system_prompt(topic)
#         logging.info(f"Generated prompt: {prompt}")  # Log the generated prompt

#         # Create the chat completion request
#         completion = client.chat.completions.create (
#             model=model,
#             messages=[
#                 {"role": "system", "content": "You are a helpful Georgian language tutor."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=300,
#             temperature=0.5,
#             top_p=0.8
#         )

#         # Access the response content directly
#         result = completion.choices[0].message.content
#         logging.info(f"OpenAI API response: {result}")  # Log response in UTF-8
#         return result
#     except Exception as e:
#         logging.error(f"Error querying ChatGPT-4 API: {e}")
#         return "Sorry, I’m having trouble generating a response right now."




from flask import Flask, request, jsonify
from lambda_function import lambda_handler  # Import your Lambda function

app = Flask(__name__)

# Define the Telegram webhook endpoint
@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    event = {
        'body': request.get_data(as_text=True)  # Capture request data as text for lambda_handler
    }
    response = lambda_handler(event, None)  # Pass the event to lambda_handler
    return jsonify(response)  # Return response to Telegram

if __name__ == "__main__":
    app.run(port=5000)

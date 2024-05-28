from dotenv import load_dotenv
from flask import Flask, request, jsonify
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import os

load_dotenv()

SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SIGNING_SECRET = os.getenv('SIGNING_SECRET')

app = Flask(__name__)

slack_client = WebClient(token=SLACK_TOKEN)
slack_events_adapter = SlackEventAdapter(SIGNING_SECRET, "/slack/events", app)

@slack_events_adapter.on("app_mention")
def handle_hello_command(event_data):
    event = event_data["event"]
    if "Hello" in event.get('text', []):
        channel = event['channel']
        message = "Hello world! I am IN42. And a bot. I am just here for testing."
        slack_client.chat_postMessage(channel=channel, text=message)

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    if data.get('type') == 'url_verification':
        challenge = data.get('challenge')
        return jsonify({'challenge': challenge}), 200
    return '', 200

if __name__ == "__main__":
    app.run(debug=False, port=5000)

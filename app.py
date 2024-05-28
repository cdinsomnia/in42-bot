from dotenv import load_dotenv
from flask import Flask, request, jsonify
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import os

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Lesen der Umgebungsvariablen
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SIGNING_SECRET = os.getenv('SIGNING_SECRET')

# Flask App initialisieren
app = Flask(__name__)

# Slack Client und Event Adapter initialisieren
slack_client = WebClient(token=SLACK_TOKEN)
slack_events_adapter = SlackEventAdapter(SIGNING_SECRET, "/slack/events", app)

# Befehl "/hello" verarbeiten
@slack_events_adapter.on("app_mention")
def handle_hello_command(event_data):
    event = event_data["event"]
    if "Hello" in event.get('text', []):
        channel = event['channel']
        message = "Hallo! Ich bin bereit, dir zu helfen."
        slack_client.chat_postMessage(channel=channel, text=message)

# Ereignis-Endpunkt für URL-Verifizierung hinzufügen
@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    if data.get('type') == 'url_verification':
        challenge = data.get('challenge')
        return jsonify({'challenge': challenge}), 200
    return '', 200

if __name__ == "__main__":
    app.run(debug=True)

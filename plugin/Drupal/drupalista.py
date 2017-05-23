"""rtmbot plugin for slack; does drupaling.

Listen for mentions of Hodor's name in channels and reply with a message.
Messages are pre-defined from a basic module import and classified by mood.
The 'mood' of reply is determined by comparing the content of the triggering
message against a library of words and human interpreted intent scoring. After
mood assignment, a message is chosen based on a dropo-type selection process
that allows for weighting of responses."""

from Drupalista.Drupalista import Drupalista
import json

config_path = '/app/plugins/python-rtmbot-drupal/config.json'
crontable = []
outputs = []

def should_respond(data, config):
    for response_string in config['responds']:
        if response_string in data['text'].lower() and data['user'].upper() in config['authorization']['users']:
            return True
    return False

def process_message(data):
    if 'text' in data:
        config = json.loads(open(config_path).read())
        if should_respond(data, config):
            drupalista = Drupalista(data, config)
            if drupalista.output:
                outputs.append([data['channel'], drupalista.output])

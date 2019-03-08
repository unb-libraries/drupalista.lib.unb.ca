"""rtmbot plugin for slack; does drupaling.

Listen for mentions of Hodor's name in channels and reply with a message.
Messages are pre-defined from a basic module import and classified by mood.
The 'mood' of reply is determined by comparing the content of the triggering
message against a library of words and human interpreted intent scoring. After
mood assignment, a message is chosen based on a dropo-type selection process
that allows for weighting of responses."""

from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
from Drupalista.Drupalista import Drupalista
import json

class DrupalistaPlugin(Plugin):

    def process_message(self, data):
        if 'text' in data.keys():
            config_path = '/app/customplugins/drupalista.json'
            config = json.loads(open(config_path).read())
            if self.should_respond(data, config):
                drupalista = Drupalista(data, config)
                if drupalista.output:
                    self.outputs.append([data['channel'], drupalista.output])

    def should_respond(self, data, config):
        for response_string in config['responds']:
            if response_string in data['text'].lower() and data['user'].upper() in config['authorization']['users']:
                return True
        return False

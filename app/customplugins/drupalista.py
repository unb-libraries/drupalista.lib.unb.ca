"""rtmbot plugin for slack; does drupaling.

Listen for mentions of Drupalista's name in channels and act on the commands in
kubernetes-deployed Drupal 8 instances."""

from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
from Drupalista.Drupalista import Drupalista
import json
import logging

class DrupalistaPlugin(Plugin):

    def process_message(self, data):
        if 'text' in data.keys():
            logger = self.get_logger()
            logging.info("{}".format(data))
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

    def get_logger(self):
        logger = logging.getLogger('simple_example')
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import json
from rasa_core_sdk import Action

import re
import subprocess


logger = logging.getLogger(__name__)


class ActionResize(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_resize"

    def run(self, dispatcher, tracker, domain):
        # entities => [{'value': '640x480', 'confidence': 1.0, 'entity': 'dimension', 'extractor': 'dim_regex'}]
        dim_entity = [e for e in tracker.latest_message.get('entities') if e['entity'] == 'dimension']
        if dim_entity:
            dim = dim_entity[0]['value']

            bash_command = f"magick logo: -resize {dim} img_output/wiz_{dim}.png"

            try:
                process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
            except Exception as e:
                error = 'Exception raised by ImageMagick.'
        else:
            error = 'No dimension specified.'

        if error:
            utter_msg_str = f'Sorry, something went wrong during resize operation... {error}.'
        else:
            utter_msg_str = f'The logo has been resized to {dim} and saved in img_output folder!'

        dispatcher.utter_message(utter_msg_str)
        return []


class ActionJoke(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_joke"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        request = json.loads(requests.get('https://api.chucknorris.io/jokes/random').text)  # make an api call
        joke = request['value']  # extract a joke from returned json response
        dispatcher.utter_message(joke)  # send the message back to the user
        return []

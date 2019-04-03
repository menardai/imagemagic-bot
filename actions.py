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
        latest_message_text = tracker.latest_message['text']

        # Extract dimension (style 640x480) from text (removing all spaces)
        # 1 or more digits, follow by 0 more white space, 'x', 0 more white space, 1 or more digits
        dim_search = re.search('(\d+)(\s*)x(\s*)(\d+)', latest_message_text, re.IGNORECASE)
        if dim_search:
            dim = dim_search.group(0)
            dim = dim.replace(" ", "")

        bash_command = f"magick logo: -resize {dim} img_output/wiz_{dim}.png"

        try:
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        except Exception as e:
            error = 'exception raised'

        utter_msg_str = 'jobs is done, look for a png file in /img_output folder!' if error is None else 'Sorry, something went wrong during resize operation...'
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

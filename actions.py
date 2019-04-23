# -*- coding: utf-8 -*-
import logging
import requests
import json
from pathlib import Path

from rasa_core_sdk import Action

import subprocess


logger = logging.getLogger(__name__)


class ActionResize(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_resize"

    def run(self, dispatcher, tracker, domain):
        # Dimension
        #   entities => [{'value': '640x480', 'confidence': 1.0, 'entity': 'dimension', 'extractor': 'dim_regex'}]
        dim_entity = [e for e in tracker.latest_message.get('entities') if e['entity'] == 'dimension']
        dim = dim_entity[0]['value'] if dim_entity else None

        # Image
        source_filename = tracker.slots['images'][0]['local_filename'] if tracker.slots.get('images') else None

        if dim and source_filename:
            source_file = Path(source_filename)
            # make sure image exists
            if source_file.is_file():
                # add dimension to filename to create the output filename:
                #   sunshine.jpg --> sunshine_1024x768.jpg
                target_name = source_file.parts[-1].replace(source_file.suffix, f"_{dim}{source_file.suffix}")

                # Execute ImageMagick command from bash
                bash_command = f"magick {source_filename} -resize {dim} img_output/{target_name}"

                try:
                    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                    output, error = process.communicate()
                except Exception as e:
                    error = 'Exception raised by ImageMagick'
            else:
                error = f'Image "{source_filename}" do not exists'
        else:
            if not dim and not source_filename:
                error = 'Missing resize dimension and image filename'
            elif not dim:
                error = 'No dimension specified'
            else:
                error = 'No image specified'

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

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
        if dim_entity:
            # priority goes to dimension specified in the latest message
            dim = dim_entity[0]['value']
        else:
            # if not specified on the latest message then look in the slots
            # because it could have been specified earlier in the conversation
            dim = tracker.slots['dimension'] if tracker.slots.get('dimension') else None

        # Image
        source_filename = tracker.slots['images'][0]['local_filename'] if tracker.slots.get('images') else None
        target_name = ""

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

        if not error:
            utter_msg_str = f'The image has been resized to {dim} and saved to: img_output/{target_name}'
        else:
            utter_msg_str = f'Sorry, something went wrong during resize operation... {error}.'

        dispatcher.utter_message(utter_msg_str)
        return []


class ActionImageAcknowledged(Action):
    def name(self):
        return "action_image_acknowledged"

    def run(self, dispatcher, tracker, domain):
        image = tracker.slots['images'][0] if tracker.slots.get('images') else None

        if image:
            source_file = Path(image['local_filename'])
            # make sure image exists
            if source_file.is_file():
                utter_msg_str = f"Got it, nice picture! Here are the details I extracted:\n" \
                                f"```  name: {image['name']}\n" \
                                f"  dimension: {image['width']}x{image['height']}\n" \
                                f"  file size: {image['size']} bytes```"
            else:
                utter_msg_str = "Oups, it looks like I had a problem saving the image you sent me :-("
        else:
            utter_msg_str = "Humm... Strange, I can't access the image you just send me :-("

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

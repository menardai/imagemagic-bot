# -*- coding: utf-8 -*-
import logging
import requests
import json
import os
import subprocess

from pathlib import Path
from rasa_sdk import Action

from rasa_sdk import ActionExecutionRejection
from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT


logger = logging.getLogger(__name__)


class ResizeImageForm(FormAction):
    """Custom form action to handle resize"""

    def name(self):
        """Unique identifier of the form"""
        return "resize_image_form"

    @staticmethod
    def required_slots(tracker):
        """A list of required slots that the form has to fill"""
        return ["images", "width", "height"]

    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        mapping = {
            "width": [self.from_entity(entity="width"),
                      self.from_text(intent="single_number_answer")],

            "height": [self.from_entity(entity="height"),
                       self.from_text(intent="single_number_answer")],

            "images": [self.from_entity(entity="images")],

            "dim_state": [],
        }
        return mapping

    @staticmethod
    def is_int(string):
        """Check if a string is an integer"""
        try:
            int(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def update_dim_state(dim_state, value):
        """Add value to dim_state string, if not already there"""
        if not dim_state:
            dim_state = value
        elif value not in dim_state:
            dim_state += value

        return dim_state

    def validate(self, dispatcher, tracker, domain):
        """Validate extracted requested slot else reject the execution of the form action """

        # extract other slots that were not requested but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))
            if not slot_values:
                # Reject form action execution if some slot was requested but nothing was extracted.
                # It will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(),
                                               f"Failed to validate slot {slot_to_fill} with action {self.name()}")

        # we'll check when validation failed in order to add appropriate utterances
        width_replaced = False
        height_replaced = False
        dim_state = tracker.slots.get('dim_state')

        for slot, value in slot_values.items():
            if slot == 'width':
                if not self.is_int(value) or int(value) <= 0:
                    dispatcher.utter_template('utter_wrong_width', tracker)
                    # validation failed, set slot to None
                    slot_values[slot] = None
                else:
                    # flag width has just replaced if dim_state indicate a width has already been set before
                    width_replaced = 'W' in dim_state if dim_state else False
                    dim_state = self.update_dim_state(dim_state, 'W')

            elif slot == 'height':
                if not self.is_int(value) or int(value) <= 0:
                    dispatcher.utter_template('utter_wrong_height', tracker)
                    # validation failed, set slot to None
                    slot_values[slot] = None
                else:
                    # flag height has just replaced if dim_state indicate a height has already been set before
                    height_replaced = 'H' in dim_state if dim_state else False
                    dim_state = self.update_dim_state(dim_state, 'H')

        slot_values['dim_state'] = dim_state

        # utter a message to acknowledge the change (if any)
        if width_replaced and height_replaced:
            dispatcher.utter_message(f"I got it, the new dimension is {slot_values['width']}x{slot_values['height']}.")
        elif width_replaced:
            dispatcher.utter_message(f"I got it, the new width is {slot_values['width']}.")
        elif height_replaced:
            dispatcher.utter_message(f"I got it, the new height is {slot_values['height']}.")

        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self, dispatcher, tracker, domain):
        """Define what the form has to do after all required slots are filled"""

        width = tracker.slots['width'] if tracker.slots.get('width') else None
        height = tracker.slots['height'] if tracker.slots.get('height') else None
        source_filename = tracker.slots['images'][0]['local_filename'] if tracker.slots.get('images') else None

        result = self.resize(width, height, source_filename)

        # utter submit template
        dispatcher.utter_message(result['message_str'])

        if result['success']:
            dispatcher.utter_attachment([{"title": f"Image resized to {result['dim_str']}",
                                          "file": f"img_output/{result['target_name']}"}])
        return []

    @staticmethod
    def resize(width, height, source_filename):
        dim_str = ""
        target_name = ""

        if width and height and source_filename:
            source_file = Path(source_filename)
            # make sure image exists
            if source_file.is_file():
                dim_str = f"{width}x{height}"

                # add dimension to filename to create the output filename:
                #   sunshine.jpg --> sunshine_1024x768.jpg
                target_name = source_file.parts[-1].replace(source_file.suffix, f"_{dim_str}{source_file.suffix}")

                # make sure output folder exists
                if not os.path.exists('img_output'):
                    os.makedirs('img_output')

                # Execute ImageMagick command from bash
                bash_command = f"magick {source_filename} -resize {dim_str} img_output/{target_name}"

                try:
                    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                    output, error = process.communicate()
                except Exception as e:
                    error = 'Exception raised by ImageMagick'

            else:
                error = f'Image "{source_filename}" do not exists'
        else:
            if not width and not source_filename:
                error = 'Missing resize dimension and image filename'
            elif not width:
                error = 'No dimension specified'
            else:
                error = 'No image specified'

        if not error:
            utter_msg_str = f'The image has been resized to {dim_str} and saved to: img_output/{target_name}'
        else:
            utter_msg_str = f'Sorry, something went wrong during resize operation... {error}.'

        return {
            "success": not error,
            "message_str": utter_msg_str,
            "dim_str": dim_str,
            "target_name": target_name,
        }


class ConvertImageToGrayScaleForm(FormAction):
    """Custom form action to handle resize"""

    def name(self):
        """Unique identifier of the form"""
        return "convert_image_to_grayscale_form"

    @staticmethod
    def required_slots(tracker):
        """A list of required slots that the form has to fill"""
        return ["images"]

    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        mapping = {
            "images": [self.from_entity(entity="images")],

            "dim_state": [],
        }
        return mapping

    @staticmethod
    def update_dim_state(dim_state, value):
        """Add value to dim_state string, if not already there"""
        if not dim_state:
            dim_state = value
        elif value not in dim_state:
            dim_state += value

        return dim_state

    def validate(self, dispatcher, tracker, domain):
        """Validate extracted requested slot else reject the execution of the form action """

        # extract other slots that were not requested but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))
            if not slot_values:
                # Reject form action execution if some slot was requested but nothing was extracted.
                # It will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(),
                                               f"Failed to validate slot {slot_to_fill} with action {self.name()}")

        # we'll check when validation failed in order to add appropriate utterances
        image_replaced = False
        dim_state = tracker.slots.get('dim_state')

        for slot, value in slot_values.items():
            if slot == 'images':
                # flag width has just replaced if dim_state indicate a width has already been set before
                image_replaced = 'I' in dim_state if dim_state else False
                dim_state = self.update_dim_state(dim_state, 'I')

        slot_values['dim_state'] = dim_state

        # utter a message to acknowledge the change (if any)
        if image_replaced:
            dispatcher.utter_message(f"Good, I got the new image!")

        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self, dispatcher, tracker, domain):
        """Define what the form has to do after all required slots are filled"""

        source_filename = tracker.slots['images'][0]['local_filename'] if tracker.slots.get('images') else None

        result = self.convert_to_grayscale(source_filename)

        # utter submit template
        dispatcher.utter_message(result['message_str'])

        if result['success']:
            dispatcher.utter_attachment([{"title": f"Image converted to grayscale",
                                          "file": f"img_output/{result['target_name']}"}])
        return []

    @staticmethod
    def convert_to_grayscale(source_filename):
        dim_str = ""
        target_name = ""

        if source_filename:
            source_file = Path(source_filename)
            # make sure image exists
            if source_file.is_file():
                # add 'grayscale' to filename to create the output filename:
                #   sunshine.jpg --> sunshine_grayscale.jpg
                target_name = source_file.parts[-1].replace(source_file.suffix, f"_grayscale{source_file.suffix}")

                # make sure output folder exists
                if not os.path.exists('img_output'):
                    os.makedirs('img_output')

                # Execute ImageMagick command from bash
                bash_command = f"magick {source_filename} -colorspace Gray img_output/{target_name}"

                try:
                    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                    output, error = process.communicate()
                except Exception as e:
                    error = 'Exception raised by ImageMagick (convert_to_grayscale)'

            else:
                error = f'Image "{source_filename}" do not exists'
        else:
            if not source_filename:
                error = 'No image specified'

        if not error:
            utter_msg_str = f'The image has been converted to grayscale and saved to: img_output/{target_name}'
        else:
            utter_msg_str = f'Sorry, something went wrong during grayscale operation... {error}.'

        return {
            "success": not error,
            "message_str": utter_msg_str,
            "target_name": target_name,
        }


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

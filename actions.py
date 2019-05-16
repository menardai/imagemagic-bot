# -*- coding: utf-8 -*-
import logging
import requests
import json
import subprocess

from pathlib import Path
from rasa_core_sdk import Action

from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk import Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT


logger = logging.getLogger(__name__)


# class ResizeForm(FormAction):
#     """Custom form action to handle resize"""
#
#     def name(self):
#         """Unique identifier of the form"""
#         return "resize_form"
#
#     @staticmethod
#     def required_slots(tracker):
#         """A list of required slots that the form has to fill"""
#
#         return ["width", "height", "images"]
#
#     def slot_mappings(self):
#         # type: () -> Dict[Text: Union[Dict, List[Dict]]]
#         """A dictionary to map required slots to
#             - an extracted entity
#             - intent: value pairs
#             - a whole message
#             or a list of them, where a first match will be picked"""
#
#         return {"cuisine": self.from_entity(entity="cuisine",
#                                             not_intent="chitchat"),
#                 # "num_people": [self.from_entity(entity="num_people",
#                 #                                 intent=["inform",
#                 #                                         "request_restaurant"]),
#                 #                self.from_entity(entity="number")],
#                 "outdoor_seating": [self.from_entity(entity="seating"),
#                                     self.from_intent(intent='affirm',
#                                                      value=True),
#                                     self.from_intent(intent='deny',
#                                                      value=False)],
#                 "preferences": [self.from_intent(intent='deny',
#                                                  value="no additional "
#                                                        "preferences"),
#                                 self.from_text(not_intent="affirm")],
#                 "feedback": [self.from_entity(entity="feedback"),
#                              self.from_text()]}
#
#     @staticmethod
#     def cuisine_db():
#         # type: () -> List[Text]
#         """Database of supported cuisines"""
#         return ["caribbean",
#                 "chinese",
#                 "french",
#                 "greek",
#                 "indian",
#                 "italian",
#                 "mexican"]
#
#     @staticmethod
#     def is_int(string):
#         """Check if a string is an integer"""
#         try:
#             int(string)
#             return True
#         except ValueError:
#             return False
#
#     def validate(self, dispatcher, tracker, domain):
#         """Validate extracted requested slot else reject the execution of the form action """
#
#         # extract other slots that were not requested but set by corresponding entity
#         slot_values = self.extract_other_slots(dispatcher, tracker, domain)
#
#         # extract requested slot
#         slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
#         if slot_to_fill:
#             slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))
#             if not slot_values:
#                 # Reject form action execution if some slot was requested but nothing was extracted.
#                 # It will allow other policies to predict another action
#                 raise ActionExecutionRejection(self.name(), "Failed to validate slot {0} with action {1}"
#                                                "".format(slot_to_fill, self.name()))
#
#         # we'll check when validation failed in order to add appropriate utterances
#         for slot, value in slot_values.items():
#             if slot == 'cuisine':
#                 if value.lower() not in self.cuisine_db():
#                     dispatcher.utter_template('utter_wrong_cuisine', tracker)
#                     # validation failed, set slot to None
#                     slot_values[slot] = None
#
#             # elif slot == 'num_people':
#             #     if not self.is_int(value) or int(value) <= 0:
#             #         dispatcher.utter_template('utter_wrong_num_people',
#             #                                   tracker)
#             #         # validation failed, set slot to None
#             #         slot_values[slot] = None
#
#             elif slot == 'outdoor_seating':
#                 if isinstance(value, str):
#                     if 'out' in value:
#                         # convert "out..." to True
#                         slot_values[slot] = True
#                     elif 'in' in value:
#                         # convert "in..." to False
#                         slot_values[slot] = False
#                     else:
#                         dispatcher.utter_template('utter_wrong_outdoor_seating', tracker)
#                         # validation failed, set slot to None
#                         slot_values[slot] = None
#
#         # validation succeed, set the slots values to the extracted values
#         return [SlotSet(slot, value) for slot, value in slot_values.items()]
#
#     def submit(self, dispatcher, tracker, domain):
#         """Define what the form has to do after all required slots are filled"""
#
#         # utter submit template
#         dispatcher.utter_template('utter_submit', tracker)
#         return []


class ActionResize(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_resize"

    def run(self, dispatcher, tracker, domain):
        # Dimension
        #   entities => [{'value': '640', 'confidence': 1.0, 'entity': 'width', 'extractor': 'dim_regex'}]
        w_entity = [e for e in tracker.latest_message.get('entities') if e['entity'] == 'width']
        h_entity = [e for e in tracker.latest_message.get('entities') if e['entity'] == 'height']
        if w_entity and h_entity:
            # priority goes to dimension specified in the latest message
            width  = w_entity[0]['value']
            height = h_entity[0]['value']
        else:
            # if not specified on the latest message then look in the slots
            # because it could have been specified earlier in the conversation
            width  = tracker.slots['width'] if tracker.slots.get('width') else None
            height = tracker.slots['height'] if tracker.slots.get('height') else None

        dim_str = ""
        target_name = ""

        # Image
        source_filename = tracker.slots['images'][0]['local_filename'] if tracker.slots.get('images') else None

        if width and height and source_filename:
            source_file = Path(source_filename)
            # make sure image exists
            if source_file.is_file():
                dim_str = f"{width}x{height}"

                # add dimension to filename to create the output filename:
                #   sunshine.jpg --> sunshine_1024x768.jpg
                target_name = source_file.parts[-1].replace(source_file.suffix, f"_{dim_str}{source_file.suffix}")

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

        dispatcher.utter_message(utter_msg_str)
        if not error:
            dispatcher.utter_attachment([{"title": f"Image resized to {dim_str}",
                                          "file": f"img_output/{target_name}"}])

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

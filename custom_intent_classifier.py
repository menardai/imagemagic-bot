import logging
import json

from rasa_nlu.components import Component

logger = logging.getLogger(__name__)


class ImageDroppedCheck(Component):
    """
    Check for a message with "[IMAGEDROPPED]" as text to return "image_dropped" intent.
    """

    name = "image_dropped_check"

    provides = ["intent", "entities"]

    requires = ["intent"]

    defaults = {}

    language_list = None

    def __init__(self, component_config=None):
        super(ImageDroppedCheck, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        pass

    def convert_to_rasa(self, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""

        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "images",
                  "extractor": "custom_intent_classifier"}
        return entity

    def process(self, message, **kwargs):
        """ message -> rasa_nlu.training_data.message.Message """

        # check for message.text starts_with '[IMAGEDROPPED]'
        if message.text.startswith('[IMAGEDROPPED]'):
            logger.info("*** Image dropped in message - force intent 'image_dropped' ***")

            # deserialized images object from message.text
            images_json = message.text[14:]

            intent = {"name": "image_dropped", "confidence": 1.0}
            message.set("intent", intent, add_to_output=True)

            message.set("intent_ranking", [intent], add_to_output=True)

            # add "images" entity
            images_dict = json.loads(images_json)
            entity = self.convert_to_rasa(images_dict, 1.0)
            message.set("entities", [entity], add_to_output=True)

    def persist(self, file_name, model_dir):
        """0.14 version - Persist this component to disk for future loading."""
        pass


class SingleNumberCheck(Component):
    """
    Check for a message with one number only (ex: "800") and return "single_number_answer" intent.
    """

    name = "single_number_check"

    provides = ["intent"]

    requires = ["intent"]

    defaults = {}

    language_list = None

    def __init__(self, component_config=None):
        super(SingleNumberCheck, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        pass

    @staticmethod
    def is_int(string):
        """Check if a string is an integer"""
        try:
            int(string)
            return True
        except ValueError:
            return False

    def process(self, message, **kwargs):
        """ message -> rasa_nlu.training_data.message.Message """

        # check for message.text with digit only
        if self.is_int(message.text):
            logger.info("*** message is a number only - force intent 'single_number_answer' ***")

            intent = {"name": "single_number_answer", "confidence": 1.0}
            message.set("intent", intent, add_to_output=True)

            message.set("intent_ranking", [intent], add_to_output=True)

    def persist(self, file_name, model_dir):
        pass

import logging

from bert_ner_dimension.model import DimensionBertNer
from rasa.nlu.components import Component

logger = logging.getLogger(__name__)


class DimNerPreprocessor(Component):
    """
    Preprocessing dimension using Bert Ner Dimension.

    Convert message like:
      'Resize my image to 640 by 480'
      'I want an image that is 640 large by 480 height'
    to
      'Resize my image to dimension'
      'I want an image that is w large by h height'

    And add an entity:
      {
         "entity": "dimension",
         "value": '640x480',    # note that the extra spaces has been removed
         "confidence": 1.0,
         "extractor": "dim_regex"
      }
    """

    name = "dim_ner"

    provides = ["entities"]

    requires = []

    defaults = {}

    language_list = None

    def __init__(self, component_config=None):
        super(DimNerPreprocessor, self).__init__(component_config)
        self.dim_ner = DimensionBertNer('bert_ner_dimension/models/dimension_ner_bert_best.pt')
        logger.info("*** BERT NER - model loaded ***")

    def train(self, training_data, cfg, **kwargs):
        pass

    @staticmethod
    def convert_to_rasa(entity, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""

        entity = {"value": value,
                  "confidence": confidence,
                  "entity": entity,
                  "extractor": "dim_regex"}
        return entity

    @staticmethod
    def is_int(string):
        """Check if a string is an integer"""
        try:
            int(string)
            return True
        except ValueError:
            return False

    def process(self, message, **kwargs):
        """ Extract dimension from message.text using a Name Entity Recognition model based on Bert. """

        # check for an existing dimension entity
        #   entities => [{'value': '640', 'confidence': 1.0, 'entity': 'width', 'extractor': 'dim_regex'}]
        w_entity = [e for e in message.data.get('entities') if e['entity'] == 'width']
        h_entity = [e for e in message.data.get('entities') if e['entity'] == 'height']

        # - ignore if the message is an image drop (see rasa/core/channels/slack.py)
        # - ignore if previous preprocessor already decoded the dimension (dim_regex.py)
        # - ignore if the text message contains only a number (user is answering a question by a single number)
        raison_to_ignore = "[IMAGEDROPPED]" in message.text or \
                           (w_entity and h_entity) or \
                           self.is_int(message.text)

        if raison_to_ignore and self.is_int(message.text):
            logger.info(f"*** BERT NER - ignore because single number only ***")

        if not raison_to_ignore:
            # ex: message.text = "resize to 640 by 480"
            dims = self.dim_ner.predict([message.text])  # dims = [{'W': 640, 'H': 480}]

            logger.info(f"*** BERT NER - dims = {dims} ***")

            entities = []
            if dims[0].get('W'):
                w_entity = self.convert_to_rasa('width',  int(dims[0]['W']), 1.0)
                entities.append(w_entity)

                # replace numbers by "width" and "height" in text message to help intent recognition
                message.text = message.text.replace(str(dims[0]['W']), 'width')

            if dims[0].get('H'):
                h_entity = self.convert_to_rasa('height', int(dims[0]['H']), 1.0)
                entities.append(h_entity)

                # replace numbers by "width" and "height" in text message to help intent recognition
                message.text = message.text.replace(str(dims[0]['H']), 'height')

            if entities:
                message.set("entities", entities, add_to_output=True)

                logger.info(f"*** BERT NER - text = {message.text} ***")

    def persist(self, file_name, model_dir):
        pass

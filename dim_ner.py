import logging

from bert_ner_dimension.model import DimensionBertNer
from rasa_nlu.components import Component

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

    def convert_to_rasa(self, entity, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""

        entity = {"value": value,
                  "confidence": confidence,
                  "entity": entity,
                  "extractor": "dim_regex"}
        return entity

    def process(self, message, **kwargs):
        """ Extract dimension from message.text using a Name Entity Recognition model based on Bert. """

        # check for an existing dimension entity
        #   entities => [{'value': '640', 'confidence': 1.0, 'entity': 'width', 'extractor': 'dim_regex'}]
        w_entity = [e for e in message.data.get('entities') if e['entity'] == 'width']
        h_entity = [e for e in message.data.get('entities') if e['entity'] == 'height']

        # Ignore if the message is an image drop.
        # Ignore if previous preprocessor already decoded the dimension (dim_regex.py)
        if "[IMAGEDROPPED]" not in message.text and not w_entity and not h_entity:
            # ex: message.text = "resize to 640 by 480"
            dims = self.dim_ner.predict([message.text])  # dims = [{'W': 640, 'H': 480}]

            logger.info(f"*** BERT NER - dims = {dims} ***")

            if dims[0].get('W') and dims[0].get('H'):

                w_entity = self.convert_to_rasa('width',  int(dims[0]['W']), 1.0)
                h_entity = self.convert_to_rasa('height', int(dims[0]['H']), 1.0)
                message.set("entities", [w_entity, h_entity], add_to_output=True)

                # replace numbers by "width" and "height" in text message to help intent recognition
                message.text = message.text.replace(str(dims[0]['W']), 'width')
                message.text = message.text.replace(str(dims[0]['H']), 'height')
                logger.info(f"*** BERT NER - text = {message.text} ***")

    def persist(self, file_name, model_dir):
        """0.14 version - Persist this component to disk for future loading."""
        pass

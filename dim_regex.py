import re

from rasa.nlu.components import Component
from rasa.nlu.extractors import EntityExtractor


class DimRegexPreprocessor(EntityExtractor):
    """
    Preprocessing dimension using regex.

    Convert message like:
      'Resize my image to 640 x 480.'
    to
      'Resize my image to dimension.'

    And add an entity:
      {
         "entity": "dimension",
         "value": '640x480',    # note that the extra spaces has been removed
         "confidence": 1.0,
         "extractor": "dim_regex"
      }
    """

    name = "dim_regex"

    provides = ["entities"]

    requires = []

    defaults = {}

    language_list = None

    def __init__(self, component_config=None):
        super(DimRegexPreprocessor, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        pass

    @staticmethod
    def convert_to_rasa(entity, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""
        entity = {
            "value": value,
            "confidence": confidence,
            "entity": entity,

            "start": 0, # dummy  value
            "end": 1,   # dummy  value
        }

        return entity

    def process(self, message, **kwargs):
        # Extract dimension (style 640x480) from message.text and remove all spaces.
        # Ignore if the message is an image drop.
        # REGEX description:
        #   1 or more digits, follow by 0 more white space, 'x', 0 more white space, 1 or more digits.
        dim_search = re.search('(\d+)(\s*)x(\s*)(\d+)', message.text, re.IGNORECASE)
        if dim_search and "[IMAGEDROPPED]" not in message.text:
            # ex: message.text = 'resize to 640 x 480.'
            dim_str = dim_search.group(0)           # '640 x 480'
            dim = dim_str.replace(" ", "").lower()  # '640x480'

            width_str = dim[:dim.index('x')]
            height_str = dim[dim.index('x') + 1:]

            w_entity = self.convert_to_rasa('width', int(width_str), 1.0)
            h_entity = self.convert_to_rasa('height', int(height_str), 1.0)

            message.text = message.text.replace(dim_str, 'dimension')  # 'resize to dimension.'

            entities = self.add_extractor_name([w_entity, h_entity])
            message.set(
                "entities", message.get("entities", []) + entities, add_to_output=True
            )

    def persist(self, file_name, model_dir):
        pass

from rasa.nlu.training_data import load_data
from rasa.nlu.model import Trainer
from rasa.nlu import config


def test_nlu_interpreter():
    #training_data = load_data("data/chitchat_nlu.md")
    training_data = load_data("data")
    trainer = Trainer(config.load("config.yml"))
    interpreter = trainer.train(training_data)
    test_interpreter_dir = trainer.persist("./tests/models", project_name="nlu")
    parsing = interpreter.parse('hello')

    assert parsing['intent']['name'] == 'greet'
    assert test_interpreter_dir

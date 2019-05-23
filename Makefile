.PHONY: clean train action-server cmdline slack x

TEST_PATH=./

help:
	@echo "    clean"
	@echo "        Remove python artifacts and build artifacts."
	@echo "    train"
	@echo "        Trains a new nlu model using the projects Rasa NLU config"
	@echo "        Trains a new dialogue model using the story training data"
	@echo "    action-server"
	@echo "        Starts the server for custom action."
	@echo "    cmdline"
	@echo "       This will load the assistant in your terminal for you to chat."


clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf docs/_build

train:
	python -m rasa train

action-server:
	python -m rasa run actions --debug

cmdline:
	python -m rasa shell

slack:
	python -m rasa run --cors "*" --credentials credentials.yml --connector slack --debug

x:
	python -m rasa x
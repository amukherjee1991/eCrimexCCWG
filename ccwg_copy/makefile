SHELL := /bin/bash
PYTHON_VERSION := 3.10
# SCRIPT := script.py
TOKEN := your_token_here
OUTPUT_CSV := output.csv

.PHONY: all setup run

all: setup run

setup:
	@echo "Setting up pipenv and installing dependencies..."
	@pipenv --python $(PYTHON_VERSION)
	@pipenv install requests

run:
	@echo "Running script..."
	@pipenv run python fetch_all_post.py $(TOKEN) $(OUTPUT_CSV)

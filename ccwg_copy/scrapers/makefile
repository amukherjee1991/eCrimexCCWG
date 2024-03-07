# Makefile

# Specify the bearer token and output file name
BEARER_TOKEN := 165c79a6a354f443edfd5119a7ae3eea637f756b
OUTPUT_DIR := output_data
OUTPUT_FILE := $(OUTPUT_DIR)/output.csv

# Default target to create output directory, setup environment, and run the script
.PHONY: all
all: setup create_output_dir run

# Target for setting up the pipenv environment and installing dependencies
.PHONY: setup
setup:
	@echo "Setting up the pipenv environment..."
	pipenv install

# Target to create the output directory
.PHONY: create_output_dir
create_output_dir:
	@echo "Creating output directory..."
	mkdir -p $(OUTPUT_DIR)

# Target for running the Python script
.PHONY: run
run:create_output_dir
	@echo "Running the Python script..."
	pipenv run python fetch_all_post.py $(BEARER_TOKEN) $(OUTPUT_FILE)

# Target for activating the pipenv shell
.PHONY: shell
shell:
	@echo "Activating the pipenv shell..."
	pipenv shell

# Target for cleaning up the environment - removes the virtualenv created by pipenv
.PHONY: clean
clean:
	@echo "Cleaning up..."
	pipenv --rm

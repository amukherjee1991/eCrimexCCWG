INPUT_DIR := ../scrapers/output_data
INPUT_FILE := $(INPUT_DIR)/output.csv
OUTPUT_DIR := ./files_by_source
# Target for setting up the pipenv environment and installing dependencies
.PHONY: setup
setup:
	@echo "Setting up the pipenv environment..."
	pipenv install
	pipreqs ./ 
	pipenv install -r requirements.txt
	

# Target to create the output directory
.PHONY: create_output_dir
create_output_dir:
	@echo "Creating output directory..."
	mkdir -p $(OUTPUT_DIR)

# Target for running the Python script
.PHONY: run
run:create_output_dir
	@echo "Running the Python script..."
	pipenv run python summary.py $(INPUT_FILE) $(OUTPUT_DIR)

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
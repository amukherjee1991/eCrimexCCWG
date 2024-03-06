# Makefile
BEARER_TOKEN := 165c79a6a354f443edfd5119a7ae3eea637f756b
# Specify the default target. When you run "make", this is what will be executed.
.PHONY: run
run: setup
	@echo "Running the Python script..."
	pipenv run python fetch_all_post.py $(BEARER_TOKEN) all_data_post.csv 

# Target for setting up the pipenv environment and installing dependencies.
.PHONY: setup
setup:
	@echo "Setting up the pipenv environment..."
	pipenv install

# Target for activating the pipenv shell.
.PHONY: shell
shell:
	@echo "Activating the pipenv shell..."
	pipenv shell

# Target for cleaning up the environment - removes the virtualenv created by pipenv.
.PHONY: clean
clean:
	@echo "Cleaning up..."
	pipenv --rm

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = e2e-customer-segmentation-rfm
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python dependencies
.PHONY: requirements
requirements:
	uv pip install -r requirements.txt
	

## Delete all compiled Python files and generated data
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	@echo "🧹 Cleaning up generated files..."
	# The '-' tells 'make' to ignore errors if files don't exist
	-rm -f data/processed/rfm_features.csv
	-rm -f data/processed/customer_segments.csv
	-rm -f models/scaler.pkl
	-rm -f models/kmeans_model.pkl
	@echo "Cleanup complete."


## Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	ruff format --check
	ruff check

## Format source code with ruff
.PHONY: format
format:
	ruff check --fix
	ruff format



## Run tests
.PHONY: test
test:
	python -m pytest tests
## Download Data from storage system
.PHONY: sync_data_down
sync_data_down:
	aws s3 sync s3://rfm-customer-segmentation-data/data/ \
		data/ 
	

## Upload Data to storage system
.PHONY: sync_data_up
sync_data_up:
	aws s3 sync data/ \
		s3://rfm-customer-segmentation-data/data 
	



## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> New uv virtual environment created. Activate with:"
	@echo ">>> Windows: .\\\\.venv\\\\Scripts\\\\activate"
	@echo ">>> Unix/macOS: source ./.venv/bin/activate"
	



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Run the entire pipeline (data -> train -> predict)
.PHONY: all
all: predict
	@echo "✅ End-to-end pipeline finished successfully."
	@echo "Final output: data/processed/customer_segments.csv"

## Make dataset (run feature engineering)
.PHONY: data
data: requirements
	@echo "--- 1. Running feature engineering (src/features.py) ---"
	$(PYTHON_INTERPRETER) src/features.py

## Train the model
.PHONY: train
train: data
	@echo "--- 2. Running model training (src/modeling/train.py) ---"
	$(PYTHON_INTERPRETER) src/modeling/train.py

## Run prediction on the dataset
.PHONY: predict
predict: train
	@echo "--- 3. Running prediction (src/modeling/predict.py) ---"
	$(PYTHON_INTERPRETER) src/modeling/predict.py

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)

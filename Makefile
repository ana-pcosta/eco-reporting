venv-dev:
	conda env create --name eco_reporting_venv_dev --file environment.yml 
	conda run -n eco_reporting_venv_dev pip install -e .[dev]

venv:
	conda env create --name eco_reporting_venv --file environment.yml
	conda run -n eco_reporting_venv pip install -e .
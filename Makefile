PYTHON ?= python3
VENV ?= .venv
VENV_PYTHON = $(VENV)/bin/python
VENV_PIP = $(VENV)/bin/pip

.PHONY: setup run clean distclean

setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install -r requirements.txt

run: setup
	$(VENV_PYTHON) Evento_simulado.py

clean:
	rm -rf __pycache__ .pytest_cache parser.out parsetab.py

distclean: clean
	rm -rf $(VENV)

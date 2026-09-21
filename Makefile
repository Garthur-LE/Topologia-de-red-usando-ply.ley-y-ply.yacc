# Makefile para Intérprete de Topologías de Stream Processing

.PHONY: setup run clean

setup:
	pip install ply

run:
	python Evento_simulado.py

clean:
	rm -f parser.out parsetab.py
	rm -rf __pycache__

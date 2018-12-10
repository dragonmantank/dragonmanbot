.PHONY: all test clean

init:
	pipenv install

run:
	python run.py

test:
	python -m unittest discover


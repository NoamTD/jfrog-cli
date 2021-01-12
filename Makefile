.PHONY: test unittests lint

deploy:
	python setup.py bdist_wheel upload -r local

test: lint
	pytest

build: lint
	pip3 install '.'

dev: lint
	pip3 install -e '.[dev]'

lint:
	flake8 src --select=E9,F63,F7,F82 --show-source --statistics
	flake8 src --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
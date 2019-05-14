.PHONY: build

test:
	python -m unittest discover

coverage:
	pip install codacy-coverage
	pip install coverage
	coverage run -m unittest discover
	coverage xml --include=ontology/* --omit=tests/*
	python-codacy-coverage -r coverage.xml

build:
	pip install -U wheel
	python setup.py bdist_wheel --python-tag py3

publish:
	pip install -U twine
	twine upload dist/* -u NashMiao -p %PYPI_PASSWORD

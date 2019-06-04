.PHONY: build

install:
	pip install --user pipenv
	pipenv install
	pipenv shell

install-mirror:
	pip install --user pipenv
	pipenv install --pypi-mirror https://mirrors.aliyun.com/pypi/simple
	pipenv shell

test:
	pipenv shell
	python -m unittest discover

coverage:
	pipenv shell
	pipenv install codacy-coverage --dev
	pipenv install coverage --dev
	coverage run -m unittest discover
	coverage xml --include=ontology/* --omit=tests/*
	python-codacy-coverage -r coverage.xml

build:
	pipenv shell
	pipenv install wheel --dev --pypi-mirror https://mirrors.aliyun.com/pypi/simple
	python setup.py bdist_wheel --python-tag py3

publish:
	pipenv shell
	pipenv install twine --dev --pypi-mirror https://mirrors.aliyun.com/pypi/simple
	twine upload dist/* -u NashMiao -p %PYPI_PASSWORD

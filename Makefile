.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with pylint"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "cover - check code coverage quickly with the default Python"
	@echo "cover-pretty - check code coverage quickly with the default Python and display as an html report in your browser"
	@echo "release - package and upload a release"
	@echo "dist - package"

clean: clean-build clean-pyc
	rm -fr htmlcov/

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	pylint publish tests examples setup.py
	flake8 publish tests examples setup.py

test:
	python setup.py test

test-all:
	tox

cover:
	pytest --cov-report term-missing --cov=publish tests/

cover-pretty:
	pytest --cov-report html --cov=publish
	open htmlcov/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

verify:
	pytest --cov-report term-missing --cov=publish tests/
	pylint publish tests examples setup.py
	flake8 publish tests examples setup.py

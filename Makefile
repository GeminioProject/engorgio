.PHONY: tests pep8 html-report

tests: pep8
	 pytest -vv --cov=engorgio --cov-report html --cov-branch tests

pep8:
	flake8 engorgio/
	flake8 --max-line-length 99 tests/

html-report:
	 python -m webbrowser file://$$PWD/htmlcov/index.html

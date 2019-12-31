.PHONY: tests html-report

tests:
	 pytest -vv --cov=engordio --cov-report html --cov-branch tests

html-report:
	 python -m webbrowser file://$$PWD/htmlcov/index.html
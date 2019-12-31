.PHONY: env tests pep8 html-report

ci: ci-env tests

dev-env:
	pipenv lock
	pipenv sync -d

ci-env:
	pipenv lock
	pipenv sync

tests: pep8
	pipenv run pytest -vv --cov=engorgio --cov-report html --cov-branch tests

pep8:
	pipenv run flake8 engorgio/
	pipenv run flake8 --max-line-length 99 tests/

html-report:
	pipenv run python -m webbrowser file://$$PWD/htmlcov/index.html

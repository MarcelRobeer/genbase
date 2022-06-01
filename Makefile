.PHONY: coverage quality

package := genbase

# Code style quality
quality:
	flake8 --config .flake8 $(package)
	python3 -m isort --line-length 120 --check-only -diff $(package)

# Coverage
coverage:
	coverage run -m pytest
	coverage html
	open htmlcov/index.html

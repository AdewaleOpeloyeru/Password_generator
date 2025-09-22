cov:
	python3 -m pytest -s --cov=src --cov-report=term-missing --cov-report=html:coverage_html tests

fmt:
	PYTHONPATH=$$(pwd) python3 -m black --check src tests

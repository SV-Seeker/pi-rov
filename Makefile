clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf

isort-check:
	isort --check

isort-fix:
	isort -rc .

flake8:
	flake8 rov/

test: clean flake8
	pytest --cov-config .coveragerc --cov-report term-missing --cov rov/ tests/

test-debug: clean
	pytest -x --pdb rov/ tests/

requirements: clean
	pipenv install --dev

# release-patch:
# 	bumpversion patch

# release-minor:
# 	bumpversion minor

# release-major:
# 	bumpversion major

# sdist: test
# 	@python setup.py sdist bdist_wheel upload

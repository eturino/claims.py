# Required executables
ifeq (, $(shell which python3))
 $(error "No python3 on PATH.")
endif
ifeq (, $(shell which pipenv))
 $(error "No pipenv on PATH.")
endif

export PYTHON_VERSION=$(shell cat .python-version| tr -d "[:space:]")

# shut up please
export PIPENV_QUIET=1

# Use relative .venv folder instead of home-folder based
export PIPENV_VENV_IN_PROJECT=1

# Ignore existing venvs
export PIPENV_IGNORE_VIRTUALENVS=1

# Make sure we are running with an explicit encoding
export LC_ALL=en_GB.UTF-8
export LANG=en_GB.UTF-8

# Set configuration folder to venv
export PYPE_CONFIG_FOLDER=$(shell pwd)/.venv/.pype-cli

export DISABLE_LOG_LEVEL=INFO

# Process variables
PY_FILES := setup.py claims tests

all: clean venv build

venv: clean
	@echo Initialize virtualenv, i.e., install required packages etc.
	pipenv install --dev --python $(PYTHON_VERSION)

clean:
	@echo Clean project base
	find . -type d \
	-name ".venv" -o \
	-name ".tox" -o \
	-name ".ropeproject" -o \
	-name ".mypy_cache" -o \
	-name ".pytest_cache" -o \
	-name "__pycache__" -o \
	-iname "*.egg-info" -o \
	-name "build" -o \
	-name "dist" \
	|xargs rm -rfv

	find . -type f \
	-name "pyproject.toml" -o \
	-name "Pipfile.lock" \
	|xargs rm -rfv

shell:
	@echo Initialize virtualenv and open a new shell using it
	pipenv shell

outdated:
	@echo Show outdated packages
	pipenv update --outdated --dev --dry-run --bare

update:
	@echo Update all libs that can be updated
	pipenv update

graph:
	@echo show the dependencies graph
	pipenv graph

test:
	@echo Run all tests in default virtualenv
	pipenv run py.test tests

testall:
	@echo Run all tests against all virtualenvs defined in tox.ini
	pipenv run tox -c setup.cfg tests

isort:
	@echo Check for incorrectly sorted imports
	pipenv run isort --profile black --check-only $(PY_FILES)

isort-apply:
	@echo Check for incorrectly sorted imports
	pipenv run isort --profile black $(PY_FILES)

mypy:
	@echo Run static code checks against source code base
	pipenv run mypy claims
	pipenv run mypy tests

black:
	@echo Run black on src and complain about issues
	pipenv run black $(PY_FILES) --check

black-apply:
	@echo Run black on src and fix any issues that it can
	pipenv run black $(PY_FILES)

lint: isort black
	@echo Run code formatting checks against source code base
	pipenv run flake8 claims tests

lint-apply: isort-apply black-apply
	@echo Run code formatting checks against source code base
	pipenv run flake8 claims tests

build: test mypy isort lint
	@echo Run setup.py-based build process to package application
	pipenv run python setup.py bdist_wheel

bump:
	@echo Bump version and change CHANGELOG
	npx standard-version

publish: all
	@echo Release to pypi.org
	pipenv run twine upload dist/*

run:
	@echo Execute claims directly
	pipenv run python -m claims

fetch-latest-boilerplate:
	@echo Fetch latest python3-boilerplate version from github
	git remote add py3template git@github.com:BastiTee/python3-boilerplate.git \
	||true
	git pull py3template master --allow-unrelated-histories ||true
	@echo ----------------------------------------------------
	@echo Resolve all merge conflicts and commit your changes!
	@echo ----------------------------------------------------

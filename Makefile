all: test

uninstall:
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

deps:
	pip install --upgrade pip build twine

install: deps
	@# Install OpenFisca-France-Inheritance for development.
	@# `make install` installs the editable version of OpenFisca-France-Inheritance.
	@# This allows contributors to test as they code.
	pip install --editable .[dev] --upgrade
	pip install openfisca-core[web-api]

build: clean deps
	@# Install OpenFisca-France-Inheritance for deployment and publishing.
	@# `make build` allows us to be be sure tests are run against the packaged version
	@# of OpenFisca-France-Inheritance, the same we put in the hands of users and reusers.
	python -m build
	pip uninstall --yes openfisca-france-inheritance
	find dist -name "*.whl" -exec pip install {}[dev] \;
	pip install openfisca-core[web-api]

check-syntax-errors:
	python -m compileall -q .

format-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	autopep8 `git ls-files | grep "\.py$$"`

check-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	flake8 `git ls-files | grep "\.py$$"`

check-yaml:
	@# check yaml style
	.github/lint-changed-yaml-tests.sh

check-all-yaml:
	@# check yaml style
	yamllint .

test: clean check-syntax-errors check-style
	@# Launch tests from openfisca_france_inheritance/tests directory (and not .) because TaxBenefitSystem must be initialized
	@# before parsing source files containing formulas.
	openfisca test --country-package openfisca_france_inheritance tests

TESTS_DIR="openfisca_inheritance/tests"
IGNORE_OPT=

check-tests-syntax:
	pyflakes $(TESTS_DIR)

test: check-tests-syntax
	nosetests -v  $(TESTS_DIR) $(IGNORE_OPT)

test-with-coverage:
	nosetests -v $(TESTS_DIR) $(IGNORE_OPT) --with-coverage --cover-package=openfisca_inheritance --cover-erase --cover-branches --cover-html

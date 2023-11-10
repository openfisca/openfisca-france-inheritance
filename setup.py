#! /usr/bin/env python

'''French inheritance legislation specific model for OpenFisca'''


from setuptools import setup, find_packages


classifiers = '''\
Development Status :: 2 - Pre-Alpha
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: POSIX
Programming Language :: Python
Topic :: Scientific/Engineering :: Information Analysis
'''

doc_lines = __doc__.split('\n')


setup(
    name = 'OpenFisca-France-Inheritance',
    version = '0.4dev',
    author = 'OpenFisca Team',
    author_email = 'contact@openfisca.fr',
    classifiers = [classifier for classifier in classifiers.split('\n') if classifier],
    description = doc_lines[0],
    keywords = 'benefit inheritance microsimulation social tax',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    long_description = '\n'.join(doc_lines[2:]),
    url = 'https://github.com/openfisca/openfisca-france-inheritance',
    extras_require = {
        'dev': [
            'autopep8 >=2.0.2, <3.0',
            'flake8 >=6.0.0, <7.0.0',
            'flake8-print >=5.0.0, <6.0.0',
            'flake8-quotes >=3.3.2',
            'pytest >=7.2.2, <8.0',
            'requests >=2.28.2, <3.0',
            'yamllint >=1.30.0, <2.0'
            ],
        },
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'OpenFisca-Core >=40.0.1, <42',
        ],
    packages = find_packages(),
    zip_safe = False,
    )

# OpenFisca-France-Inheritance

## [EN] Introduction

OpenFisca is a versatile microsimulation free software. This repository contains the OpenFisca model of the French inheritance legislation system. Therefore, the working language here is French. You can however check the [general OpenFisca documentation](https://openfisca.org/doc/) in English!

> If you are interested in other taxes in France, you may also want to look at the [openfisca-france](https://github.com/openfisca/openfisca-france) tax and benefit system.

## [FR] Introduction

[OpenFisca](https://www.openfisca.fr/) est un logiciel libre de micro-simulation. Ce dépôt contient la modélisation du système des donations et successions en France. Pour plus d'information sur les fonctionnalités et la manière d'utiliser OpenFisca, vous pouvez consulter la [documentation générale](https://openfisca.org/doc/).

> Dans le cas où vous seriez intéressé·e par d'autres impositions en France, sachez qu'il existe également un modèle socio-fiscal [openfisca-france](https://github.com/openfisca/openfisca-france).

## Installation

Ce paquet requiert [Python 3.11](https://www.python.org/downloads/release/python-31111/) (ou a minima Python 3.9) et [pip](https://pip.pypa.io/en/stable/installing/).

Pour que l'installation d' n'interfère pas avec vos autres projets Python en cours, nous vous conseillons de créer un environnement virtuel dans lequel vous placerez les dépendances du dépôt.

Avant de passer à la suite, la commande suivante exécutée dans un terminal shell doit indiquer `Python 3.11.*` (ou, a minima, Python 3.9.*):

```sh
python --version
```

Si vous souhaitez contribuer au code source, nous vous conseillons de l'installer en local sur votre ordinateur avec : 

```sh
git clone git@github.com:openfisca/openfisca-france-inheritance.git
```

### Installer avec Pew pour la contribution (mode développement)

Si vous souhaitez suivre les mêmes recommendantions que pour le dépôt `openfisca-france`, vous pouvez vous appuyer sur l'outil `pew` pour la gestion des environnements virtuels. Suivre alors la [section dédiée du README openfisca-france](https://github.com/openfisca/openfisca-france/blob/master/README.md#installez-un-environnement-virtuel-avec-pew).

Puis, dans l'environnement virtuel activé, exécuter la commande suivante : 

```sh
pip install --editable .[dev] --upgrade
pip install openfisca-core  
# ou pip install openfisca-core[web-api] si vous souhaitez exécuter la web API openfisca
```

`OpenFisca-France-Inheritance` sera installé en mode éditable auprès des autres dépendances par défaut. Toujours dans l'environnement virtuel activé, vous pouvez alors vérifier ce qui a été installé avec : 

```sh
pip list
```

### Installer avec Poetry pour la contribution (mode développement)

Afin d'utiliser un unique outil pour la gestion des environnements virtuels et de l'installation, vous pouvez vous appuyer sur [Poetry](https://python-poetry.org).

> En savoir plus sur l'[installation de Poetry sur sa documentation officielle](https://python-poetry.org/docs/#installation).

En local, à la racine du dépôt :
```sh
poetry install --extras dev
```

Ceci créera un environnement virtuel. Dans cet environnement isolé, `OpenFisca-France-Inheritance` sera installé en mode éditable auprès des autres dépendances par défaut. Vous pouvez alors vérifier ce qui a été installé avec : 

```sh
poetry run pip list
```

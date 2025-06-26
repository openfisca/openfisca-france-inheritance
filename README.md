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

## Exécuter l'API web

> Mémo : les librairies contenant l'API web sont référencées par le fichier `pyproject.toml` au travers de l'option `web-api` d'`openfisca-core[web-api]`. On suppose ici qu'elles ont été installées à l'étape précédente.

Pour exécuter l'API web et tester des requêtes, deux terminaux sont utilisés : 
* un terminal permettant d'exécuter l'API web avec la commande `openfisca serve`
* un terminal permettant d'envoyer des requêtes à l'API web (ou votre outil favori d'envoi de requêtes)


### Exécution avec `openfisca serve`

Dans un premier terminal, exécuter l'API web requiert la commande `openfisca serve` qui a été installée sur votre machine à l'étape précédente.

Il est par exemple possible de tester sa bonne présence en consultant ses options disponibles avec : 
```sh
$ poetry run openfisca serve --help

usage: openfisca serve [-h] [-c COUNTRY_PACKAGE] [-e [EXTENSIONS ...]]
                       [-r [REFORMS ...]] [-p PORT]
                       [--tracker-url TRACKER_URL]
                       [--tracker-idsite TRACKER_IDSITE]
                       [--tracker-token TRACKER_TOKEN]
                       [--welcome-message WELCOME_MESSAGE]
                       [-f CONFIGURATION_FILE]

options:
  -h, --help            show this help message and exit
  -c COUNTRY_PACKAGE, --country-package COUNTRY_PACKAGE
                        country package to use. If not provided, an automatic
                        detection will be attempted by scanning the python
                        packages installed in your environment which name
                        contains the word "openfisca".
  ...
```
où `poetry run` permet d'exécuter la commande qui suit - `openfisca serve --help` - dans l'environnement virtuel où les librairies Python du dépôt ont été installées.

Puis exécuter l'API web avec la commande suivante : 

```sh
$ poetry run openfisca serve --country-package openfisca_france_inheritance 

[2025-04-11 14:40:23 +0200] [92209] [INFO] Starting gunicorn 21.2.0
[2025-04-11 14:40:23 +0200] [92209] [INFO] Listening at: http://127.0.0.1:5000 (92209)
[2025-04-11 14:40:23 +0200] [92209] [INFO] Using worker: sync
[2025-04-11 14:40:23 +0200] [92381] [INFO] Booting worker with pid: 92381
[2025-04-11 14:40:23 +0200] [92382] [INFO] Booting worker with pid: 92382
[2025-04-11 14:40:23 +0200] [92383] [INFO] Booting worker with pid: 92383
```

Comme l'indique la commande, l'API est par défaut disponible sur `http://127.0.0.1:5000`.
Pour en savoir plus sur les différentes options de configuration de l'API telles que la définition du port, il est également possible de consulter la documentation officielle : https://openfisca.org/doc/openfisca-python-api/openfisca_serve.html

### Exemple de requête

Dans un second terminal, il est possible d'utiliser la commande `curl` afin d'envoyer une requête de calcul à l'endpoint `/calculate`.

> Pour en savoir plus sur les endpoints disponibles consulter la documentation officielle openfisca : https://openfisca.org/doc/openfisca-web-api/endpoints.html 

Un exemple de requête (payload) `donation.json` est disponible dans le répertoire `openfisca_france_inheritance/situation_examples/`. Afin de l'envoyer à `/calculate`, exécuter : 

```sh
$ cd openfisca_france_inheritance/situation_examples/
$ curl -X POST http://127.0.0.1:5000/calculate -H 'Content-Type: application/json' -d @donation.json
```

> ou `curl -X POST http://127.0.0.1:5000/calculate -H 'Content-Type: application/json' -d @donation.json | jq` utilisant `jq` pour la mise en forme de l'affichage.

L'API répondra en complétant la question qui a été envoyée : les `null` seront remplacés par les valeurs calculées. 

Exemple de réponse : 

```json
{
  "donations": {
    "donation_1": {
      "actif_brut_donne": {
        "ETERNITY": 200000
      },
      "donateur": "Camille",
      "enfant_donataire": "Claude"
    }
  },
  "individus": {
    "Camille": {
      "age": {
        "2025-01": "60"
      }
    },
    "Claude": {
      "abattement_plafond": {
        "2025-01": 100000.0
      },
      "age": {
        "2025-01": "40"
      },
      "droits_donation": {
        "2025-01": 11821.35
      },
      "exoneration_don_familial": {
        "2025-01": 31865.0
      }
    }
  },
  "successions": {}
}
```

Pour en savoir plus sur l'usage de l'endpoint `/calculate`, consulter : https://openfisca.org/doc/openfisca-web-api/input-output-data.html

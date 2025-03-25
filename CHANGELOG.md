# CHANGELOG

### 0.5.2 [#3](https://github.com/openfisca/openfisca-france-inheritance/pull/3)

* Amélioration technique.
* Périodes concernées : non applicable
* Zones impactées : non applicable
* Détails :
  - Reporte le contenu de `COPYING` dans `LICENSE` mettant en cohérence la licence à AGPL v3
  - Initialise une configuration d'intégration continue pour GitHub Actions dans `.github/workflows/workflow.yml`
    * Définit un job de `build` et un job de `test-yaml`
  - Ajoute des modèles d'issue et de demande de tirage GitHub

### 0.5.1 [#2](https://github.com/openfisca/openfisca-france-inheritance/pull/2)

* Changement mineur
* Périodes concernées : toutes.
* Zones impactées : -
* Détails :
  - Documente l'installation en mode développement
  - Ajoute les fichiers de contribution CHANGELOG.md et CONTRIBUTING.md

## 0.5.0 [#1](https://github.com/openfisca/openfisca-france-inheritance/pull/1)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : 
  - `openfisca_france_inheritance/scenarios.py`
* Détails :
  - Migre d'un `setup.py` à `pyproject.toml`
  - Supprime `openfisca_france_inheritance/scenarios.py` et `openfisca_france_inheritance/scripts/sandbox.py`
  - Ajoute un répertoire `tests` et des tests YAML de donations et successions
  - Commence l'adaptation d'un `Makefile` sur la base de celui d'`openfisca-france`

> Ce dépôt fait suite à : https://github.com/benjello/openfisca-inheritance

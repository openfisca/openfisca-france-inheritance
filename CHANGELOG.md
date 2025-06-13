# CHANGELOG

# 1.0.0 [#5](https://github.com/openfisca/openfisca-france-inheritance/pull/5)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : 
  - `parameters/*`
* Détails :
  - Harmonise l'ensemble des paramètres du modèles avec les barèmes IPP
    * Ajoute l'ensemble des paramètres donations et succession des barèmes IPP
    * Insère les paramètres pré-existants d'openfisca_france_inheritance dans l'arborescence IPP
    * Passe en barèmes les paramètres de calcul de droits pour conjoint, pacs et descendant en ligne directe dans `parameters/droits_mutation_titre_gratuit/bareme/`
    * Corrige certaines références et dates d'entrée en vigueur
  - Permet à tous les tests de s'achever sans erreur en corrigeant `tests/donation/celib_frere_don.yaml`, `tests/succession/veuf_2_enfants.yaml`, et `tests/succession/homme_marie_3_enf.yaml`
  - Met à jour les formules de `droits` et `droits_sur_succession` suite au renommage de paramètres et en cohérence avec les tests
* Migration :
  - Identifier les renommages et déplacements de paramètres avec la commande : `git log --first-parent --diff-filter=R --summary 92f7b597b^..63ae897d5`
  - Identifier les ajouts de paramètres avec : `git log --first-parent --diff-filter=A --summary 92f7b597b^..63ae897d5`

### 0.5.3 [#6](https://github.com/openfisca/openfisca-france-inheritance/pull/6)

* Amélioration technique.
* Détails :
  - Ajout de la validation des paramètres

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

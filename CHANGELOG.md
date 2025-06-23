# CHANGELOG

# 

> Initialement proposé sur [openfisca-france #2418](https://github.com/openfisca/openfisca-france/pull/2418)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 31/07/2011.
* Zones impactées : 
  - `entities.py`
  - `variables/individu.py`
  - `variables/donation.py`
  - `variables/succession.py`
  - `parameters/droits_mutation_titre_gratuit/abattement/*`
  - `parameters/droits_mutation_titre_gratuit/bareme/*`
  - `parameters/droits_mutation_titre_gratuit/exoneration/*`
* Détails :
  - Ajoute le calcul des donations incluant les exonérations pour don familial et les abattements
    * À l'entité Donation
      - Renomme le rôle `arrière_grand_parent_donataire` en `arriere_grand_parent_donataire`
      - Ajoute les rôles `parent_4eme_degre_donataire` et `non_parent_donataire`
    * Ajoute `parameters/droits_mutation_titre_gratuit/abattement/ascendant.yaml`
    * Ajoute `parameters/droits_mutation_titre_gratuit/exoneration/`
    * Aux individus 
      - Ajoute `age`, `is_donateur`, `is_donataire`, `is_petit_enfant_donataire`, `is_arriere_petit_enfant_donataire`, `is_neveu_niece_donataire`, `existe_descendant_direct`
      - Migre `is_enfant_donataire` de nombre à booléen
      - Migre `role_representant` du type `TypesRoleRepresentant` à `LienParente`
      - Renomme `droits` en `droits_mutation` et ajoute `droits_succession`
      - Ajoute `droits_donation` et ses dispositifs internes `exoneration_don_familial`, `actif_imposable_donataire`, `abattement_plafond`, `actif_taxable_donataire`
    * Aux donations
      - Ajoute `actif_brut` comme premier niveau d'actif propre impliqué dans une donation
      - Renomme `actif_propre_don` en `actif_brut_donne`, part d'`actif_brut` par donataire
      - Ajoute `existe_descendant_direct_donateur`
      - Corrige le calcul d'`actif_imposable_don`

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

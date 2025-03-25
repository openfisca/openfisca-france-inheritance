# Contribuer à OpenFisca-France-Inheritance

Avant tout, merci de votre volonté de contribuer au bien commun qu'est OpenFisca !

Afin de faciliter la réutilisation d'OpenFisca et d'améliorer la qualité du code, les contributions à OpenFisca suivent certaines règles.

Certaines règles sont communes à tous les dépôts OpenFisca et sont détaillées dans [la documentation générale](https://openfisca.org/doc/contribute/guidelines.html).


## Format du Changelog

Les évolutions d'OpenFisca-France-Inheritance doivent pouvoir être comprises par des réutilisateurs qui n'interviennent pas nécessairement sur le code. Le Changelog, rédigé en français, se doit donc d'être le plus explicite possible.

Chaque évolution sera documentée par les éléments suivants :

- Sur la première ligne figure en guise de titre le numéro de version, et un lien vers la Pull Request introduisant le changement. Le niveau de titre doit correspondre au niveau d'incrémentation de la version.

- La deuxième ligne indique de quel type de changement il s'agit. Les types possibles sont :
  - `Évolution du système socio-fiscal` : Amélioration, correction, mise à jour d'un calcul. Impacte les réutilisateurs intéressés par les calculs.
  - `Amélioration technique` : Amélioration des performances, évolution de la procédure d'installation, de la syntaxe des formules… Impacte les réutilisateurs rédigeant des règles et/ou déployant leur propre instance.
  - `Correction d'un crash` : Impacte tous les réutilisateurs.
  - `Changement mineur` : Refactoring, métadonnées… N'a aucun impact sur les réutilisateurs.

- **Dans le cas d'une `Évolution du système socio-fiscal`** , il est ensuite précisé :
  - Les périodes concernées par l'évolution. Les dates doivent être données au jour près pour lever toute ambiguïté : on écrira `au 01/01/2017` et non `pour 2017` (qui garde une ambiguïté sur l'inclusion de l'année en question).
  - Les zones du modèle de calcul impactées. Ces zones correspondent à l'arborescence des fichiers dans le modèle, sans l'extension `.py`.

> Par exemple :
> - Périodes concernées : Jusqu'au 31/12/2015.
> - Zones impactées : `variables/donation.py`

- Enfin, dans tous les cas hors `Changement mineur`, les corrections apportées doivent être explicitées de détails donnés d'un point de vue fonctionnel : dans quel cas d'usage constatait-on un erreur / un problème ? Quelle nouvelle fonctionalité est disponible ? Quel nouveau comportement est adopté ?

Dans le cas où une Pull Request contient plusieurs évolutions distinctes, plusieurs paragraphes peuvent être ajoutés au Changelog.

## Debug des tests YAML avec VS Code

Si vous souhaitez utiliser le debugger de VS Code avec les tests YAML, par exemple pour investiguer la commande suivante :

`openfisca test --country-package openfisca_france_inheritance tests/donation/veuf_2_enfants_don.yaml`

Il faut créer un fichier de configuration `.vscode/launch.json` avec le contenu suivant :

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Debug current YAML test file",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/.venv/bin/openfisca",
            "args": [
                "test",
                "--country-package",
                "openfisca_france_inheritance",
                "${file}"
            ],
            "console": "integratedTerminal",
            "justMyCode": false,
        }
    ]
}
```

Puis dans VS Code, ouvrir le fichier YAML à debugger, et lancer le debugger avec la configuration `Python: Debug current YAML test file` dans l'onglet _Run and Debug_ à gauche.

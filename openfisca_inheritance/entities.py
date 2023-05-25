from openfisca_core.entities import build_entity


Individu = build_entity(
    key = "individu",
    plural = "individus",
    label = 'Une personne/un individu',
    is_person = True,
    )


Succession = build_entity(
    key = "succession",
    plural = "successions",
    label = 'Les individus impliqués dans une succession.',
    roles = [
        {
            'key': 'decede',
            'label': 'Décédé',
            'max': 1,
            'doc': 'La personne décédé.'
            },
        {
            'key': 'epoux_survivant',
            'label': 'Époux survivant',
            'max': 1,
            'doc': "L'époux de la personne décédé."
            },
        {
            'key': 'enfant_survivant',
            'plural': 'enfants_survivants',
            'label': 'Enfant survivant',
            'doc': "Les enfants vivants au décès de leur parent décédé."
            },
        {
            'key': 'collateral',
            'plural': 'collateraux',
            'label': 'Collatéral',
            'doc': "Les collatéraux du décédé."
            }
        ]
    )


Donation = build_entity(
    key = "donation",
    plural = "donations",
    label = 'Les individus impliqués dans une donation.',
    roles = [
        {
            'key': 'decede',
            'label': 'Décédé',
            'max': 1,
            'doc': 'La personne décédé.'
            },
        {
            'key': 'epoux_survivant',
            'label': 'Époux survivant',
            'max': 1,
            'doc': "L'époux de la personne décédé."
            },
        {
            'key': 'enfant_survivant',
            'plural': 'enfants_survivants',
            'label': 'Enfant survivant',
            'doc': "Les enfants vivants au décès de leur parent décédé."
            },
        {
            'key': 'collateral',
            'plural': 'collateraux',
            'label': 'Collatéral',
            'doc': "Les collatéraux du décédé."
            },
        {
            'key': 'legatatire',
            'plural': 'legatatires',
            'label': 'Légataire',
            'doc': "Les légattaires du décédé."
            },
        ]
    )


entities = [Individu, Succession, Donation]

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
            'key': 'pacse',
            'label': 'Partenaires liés par un PACS',
            'max': 1,
            'doc': "Le partenaire,lié par un PACS, de la personne décédé."
            },
        {
            'key': 'enfant_survivant',
            'label': 'Enfants survivants',
            'doc': "Les enfants vivants au décès de leur parent décédé."
            },
        {
            'key': 'frere_soeur',
            'label': 'Frères et Soeurs',
            'doc': "Les frères et soeurs vivants du décédé."
            },
        {
            'key': 'parent',
            'label': 'Parents',
            'doc': "Les parents vivants du décédé."
            },
        {
            'key': 'grand-parent',
            'label': 'Grands-Parents',
            'doc': "Les grands-parents vivants du décédé."
            },
        {
            'key': 'arrière_grand_parent',
            'label': 'Arrières-Grands-Parents',
            'doc': "Les arrières-grands-parents vivants du décédé."
            },
        {
            'key': 'neveu_niece',
            'label': 'Neveux et Nièces',
            'doc': "Les neveux et nièces vivants du décédé."
            },
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
            'key': 'pacse',
            'label': 'Partenaires liés par un PACS',
            'max': 1,
            'doc': "Le partenaire,lié par un PACS, de la personne décédé."
            },
        {
            'key': 'enfant_survivant',
            'label': 'Enfants survivants',
            'doc': "Les enfants vivants au décès de leur parent décédé."
            },
        {
            'key': 'frere_soeur',
            'label': 'Frères et Soeurs',
            'doc': "Les frères et soeurs vivants du décédé."
            },
        {
            'key': 'parent',
            'label': 'Parents',
            'doc': "Les parents vivants du décédé."
            },
        {
            'key': 'grand-parent',
            'label': 'Grands-Parents',
            'doc': "Les grands-parents vivants du décédé."
            },
        {
            'key': 'arrière_grand_parent',
            'label': 'Arrières-Grands-Parents',
            'doc': "Les arrières-grands-parents vivants du décédé."
            },
        {
            'key': 'neveu_niece',
            'label': 'Neveux et Nièces',
            'doc': "Les neveux et nièces vivants du décédé."
            },
        {
            'key': 'petit_enfant_survivant',
            'label': 'Petits-Enfants survivants',
            'doc': "Les petits-enfants vivants au décès de leur parent décédé."
            },
        {
            'key': 'arriere_petit_enfant_survivant',
            'label': 'Arrières-Petits-Enfants survivants',
            'doc': "Les arrières-petits-enfants vivants au décès de leur parent décédé."
            },
        ]
    )


entities = [Individu, Succession, Donation]

from openfisca_core.entities import build_entity


Individu = build_entity(
    key = 'individu',
    plural = 'individus',
    label = 'Une personne/un individu',
    is_person = True,
    )


Succession = build_entity(
    key = 'succession',
    plural = 'successions',
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
            'doc': 'Le partenaire,lié par un PACS, de la personne décédé.'
            },
        {
            'key': 'enfant_survivant',
            'label': 'Enfants survivants',
            'doc': 'Les enfants vivants au décès de leur parent décédé.'
            },
        {
            'key': 'frere_soeur',
            'label': 'Frères et Soeurs',
            'doc': 'Les frères et soeurs vivants du décédé.'
            },
        {
            'key': 'parent',
            'label': 'Parents',
            'doc': 'Les parents vivants du décédé.'
            },
        {
            'key': 'grand-parent',
            'label': 'Grands-Parents',
            'doc': 'Les grands-parents vivants du décédé.'
            },
        {
            'key': 'arrière_grand_parent',
            'label': 'Arrières-Grands-Parents',
            'doc': 'Les arrières-grands-parents vivants du décédé.'
            },
        {
            'key': 'neveu_niece',
            'label': 'Neveux et Nièces',
            'doc': 'Les neveux et nièces vivants du décédé.'
            },
        {
            'key': 'autre_survivant',
            'label': 'Tiers',
            'doc': 'Légation du patrimoine à un tiers hors du cercle familiale.'
            },
        ]
    )


Donation = build_entity(
    key = 'donation',
    plural = 'donations',
    label = 'Les individus impliqués dans une donation.',
    roles = [
        {
            'key': 'donateur',
            'label': 'Donateur',
            'max': 1,
            'doc': 'La personne donatrice.'
            },
        {
            'key': 'epoux_donataire',
            'label': 'Époux donataire',
            'max': 1,
            'doc': "L'époux de l'individu donateur."
            },
        {
            'key': 'pacs_donataire',
            'label': 'Partenaires liés par un PACS',
            'max': 1,
            'doc': "Le partenaire, lié par un PACS, de l'individu donateur."
            },
        {
            'key': 'enfant_donataire',
            'label': 'Enfants donataires',
            'doc': 'Les enfants vivants au décès de leur parent donateur.'
            },
        {
            'key': 'frere_soeur_donataire',
            'label': 'Frères et Soeurs donataires',
            'doc': 'Les frères et soeurs vivants du donateur.'
            },
        {
            'key': 'parent_donataire',
            'label': 'Parents donataires',
            'doc': 'Les parents vivants du donateur.'
            },
        {
            'key': 'grand_parent_donataire',
            'label': 'Grands-Parents donataires',
            'doc': 'Les grands-parents vivants du donateur.'
            },
        {
            'key': 'arrière_grand_parent_donataire',
            'label': 'Arrières-Grands-Parents donataires',
            'doc': 'Les arrières-grands-parents vivants du donateur.'
            },
        {
            'key': 'neveu_niece_donataire',
            'label': 'Neveux et Nièces donataires',
            'doc': 'Les neveux et nièces vivants du donateur.'
            },
        {
            'key': 'petit_enfant_donataire',
            'label': 'Petits-Enfants donataires',
            'doc': 'Les petits-enfants vivants au décès de leur parent donateur.'
            },
        {
            'key': 'arriere_petit_enfant_donataire',
            'label': 'Arrières-Petits-Enfants donataires',
            'doc': 'Les arrières-petits-enfants vivants au décès de leur parent donateur.'
            },
        {
            'key': 'parent_4eme_degre',
            'label': 'Parents de 4ème degré donataires',
            'doc': 'Les parents de 4ème degré vivants au décès de leur parent donateur.'
            },
        ]
    )


entities = [Individu, Succession, Donation]

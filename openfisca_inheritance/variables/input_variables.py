from datetime import date
from openfisca_core.model_api import *
from openfisca_core.columns import DateCol, EnumCol, float, IntCol, StrCol
from openfisca_core.enumerations import Enum
from openfisca_core.formulas import reference_input_variable

from .entities import Individus, Successions  # Donations


ROLE_REPRESENTANT = Enum([
    'décédé',  # 0 cas spécial
    'enfant',  # 1
    'époux',  # 2
    'parent',  # 3
    ])
DECEDE = ROLE_REPRESENTANT[u'décédé']
ENFANT = ROLE_REPRESENTANT[u'enfant']
EPOUX = ROLE_REPRESENTANT[u'époux']
PARENT = ROLE_REPRESENTANT[u'parent']

QUISUCC = Enum([
    'decede',
    'succedant',
    ])


#reference_input_variable(
#    value_type = float,
#    entity = Successions,
#    label = "Actif de communauté",
#    name = 'actif_de_communaute',
#    )

#reference_input_variable(
#    value_type = float,
#    entity = Successions,
#    label = "Passif de communauté",
#    name = 'passif_de_communaute',
#    )

reference_input_variable(
    value_type = float,
    entity = Successions,
    label = "Actif de Communauté",
    name = 'actif_de_communaute',
    )

reference_input_variable(
    value_type = float,
    entity = Successions,
    label = "Actif propre",
    name = 'actif_propre',
    )

reference_input_variable(
    value_type = float,
    entity = Successions,
    label = "Assurance Vie",
    name = 'assurance_vie',
    )

reference_input_variable(
    value_type = DateCol(default = date(1, 1, 1)),
    entity = Individus,
    label = "Date du décès",
    name = 'date_deces',
    )

# reference_input_variable(
#     value_type = IntCol,
#     entity = Donations,
#     label = "Année de la donation",
#     name = 'date',
#     )

# reference_input_variable(
#     value_type = float,
#     entity = Donations,
#     label = "Don",
#     name = 'don',
#     )

reference_input_variable(
    value_type = StrCol,
    entity = Individus,
    label = "Identifiant de l'individu",
    name = 'id',
    )

reference_input_variable(
    value_type = StrCol,
    entity = Individus,
    label = "Identifiant de l'individu représenté par cet individu",
    name = 'id_represente',
    )

reference_input_variable(
    value_type = IntCol,
    entity = Individus,
    label = "Donation auquel appartient l'individu",
    name = 'iddon',
    )

reference_input_variable(
    value_type = IntCol,
    entity = Individus,
    label = "Succession auquel appartient l'individu",
    name = 'idsucc',
    )

reference_input_variable(
    value_type = IntCol,
    entity = Individus,
    label = "Index de l'individu représenté par cet individu",
    name = 'index_represente',
    )

reference_input_variable(
    value_type = float,
    entity = Successions,
    label = "Part epoux",
    name = 'part_epoux',
    )

reference_input_variable(
    value_type = float,
    entity = Successions,
    label = "Passif de Communauté",
    name = 'passif_de_communaute',
    )

reference_input_variable(
    value_type = float,
    entity = Successions,
    label = "Passif propre",
    name = 'passif_propre',
    )

reference_input_variable(
    value_type = EnumCol(QUISUCC),
    entity = Individus,
    label = "Role de l'individu dans la succession",
    name = 'quisucc',
    )

# reference_input_variable(
#     value_type = EnumCol(QUIDON),
#     entity = Individus,
#     label = "Role de l'individu dans la donation",
#     name = 'quidon',
#     )

reference_input_variable(
    value_type = EnumCol(ROLE_REPRESENTANT),
    entity = Individus,
    label = "Rôle de l'individu par rapport au représenté",
    name = 'role_representant',
    )


#reference_input_variable(
#    value_type = StrCol,
#    entity = Individus,
#    label = "Identifiant de l'individu",
#    name = 'id',
#    )

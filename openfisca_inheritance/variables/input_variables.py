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


#class actif_de_communaute(Variable):
#    value_type = float,
#    entity = Successions,
#    label = "Actif de communauté",
#
#class passif_de_communaute(Variable):
#    value_type = float,
#    entity = Successions,
#    label = "Passif de communauté",
#
class actif_de_communaute(Variable):
    value_type = float,
    entity = Successions,
    label = "Actif de Communauté",

class actif_propre(Variable):
    value_type = float,
    entity = Successions,
    label = "Actif propre",

class assurance_vie(Variable):
    value_type = float,
    entity = Successions,
    label = "Assurance Vie",

class date_deces(Variable):
    value_type = DateCol(default = date(1, 1, 1)),
    entity = Individus,
    label = "Date du décès",

# class date(Variable):
#     value_type = IntCol,
#     entity = Donations,
#     label = "Année de la donation",
#
# class don(Variable):
#     value_type = float,
#     entity = Donations,
#     label = "Don",
#
class id(Variable):
    value_type = StrCol,
    entity = Individus,
    label = "Identifiant de l'individu",

class id_represente(Variable):
    value_type = StrCol,
    entity = Individus,
    label = "Identifiant de l'individu représenté par cet individu",

class iddon(Variable):
    value_type = IntCol,
    entity = Individus,
    label = "Donation auquel appartient l'individu",

class idsucc(Variable):
    value_type = IntCol,
    entity = Individus,
    label = "Succession auquel appartient l'individu",

class index_represente(Variable):
    value_type = IntCol,
    entity = Individus,
    label = "Index de l'individu représenté par cet individu",

class part_epoux(Variable):
    value_type = float,
    entity = Successions,
    label = "Part epoux",

class passif_de_communaute(Variable):
    value_type = float,
    entity = Successions,
    label = "Passif de Communauté",

class passif_propre(Variable):
    value_type = float,
    entity = Successions,
    label = "Passif propre",

class quisucc(Variable):
    value_type = EnumCol(QUISUCC),
    entity = Individus,
    label = "Role de l'individu dans la succession",

# class quidon(Variable):
#     value_type = EnumCol(QUIDON),
#     entity = Individus,
#     label = "Role de l'individu dans la donation",
#
class role_representant(Variable):
    value_type = EnumCol(ROLE_REPRESENTANT),
    entity = Individus,
    label = "Rôle de l'individu par rapport au représenté",


#class id(Variable):
#    value_type = StrCol,
#    entity = Individus,
#    label = "Identifiant de l'individu",
#

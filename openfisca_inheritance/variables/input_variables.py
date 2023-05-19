from openfisca_core.model_api import *

from openfisca_inheritance.entities import Individu, Succession  # Donations


class TypesRoleRepresentant(Enum):
    __order__ = 'decede enfant epoux parent'  # Needed to preserve the enum order in Python 2
    decede = "Personne décédée"
    enfant = "Enfant"
    epoux = "Époux"
    parent = "Parent"


class TypesRoleSuccession(Enum):
    __order__ = 'decede succedant'  # Needed to preserve the enum order in Python 2
    decede = "Personne décédée"
    succedant = "Succédant"

class actif_de_communaute(Variable):
    value_type = float
    entity = Succession
    label = "Actif de Communauté"
    definition_period = ETERNITY

class actif_propre(Variable):
    value_type = float
    entity = Succession
    label = "Actif propre"
    definition_period = ETERNITY

class assurance_vie(Variable):
    value_type = float
    entity = Succession
    label = "Assurance Vie"
    definition_period = ETERNITY

class date_deces(Variable):
    value_type = date
    entity = Individu
    label = "Date du décès"
    definition_period = ETERNITY

# class date(Variable):
#     value_type = int
#     entity = Donations
#     label = "Année de la donation"
#     definition_period = ETERNITY
#
# class don(Variable):
#     value_type = float
#     entity = Donations
#     label = "Don"
#     definition_period = ETERNITY

class id(Variable):
    value_type = str
    entity = Individu
    label = "Identifiant de l'individu"
    definition_period = ETERNITY

class id_represente(Variable):
    value_type = str
    entity = Individu
    label = "Identifiant de l'individu représenté par cet individu"
    definition_period = ETERNITY

class iddon(Variable):
    value_type = int
    entity = Individu
    label = "Donation auquel appartient l'individu"
    definition_period = ETERNITY

class idsucc(Variable):
    value_type = int
    entity = Individu
    label = "Succession auquel appartient l'individu"
    definition_period = ETERNITY

class index_represente(Variable):
    value_type = int
    entity = Individu
    label = "Index de l'individu représenté par cet individu"
    definition_period = ETERNITY

class part_epoux(Variable):
    value_type = float
    entity = Succession
    label = "Part epoux"
    definition_period = ETERNITY

class passif_de_communaute(Variable):
    value_type = float
    entity = Succession
    label = "Passif de Communauté"
    definition_period = ETERNITY

class passif_propre(Variable):
    value_type = float
    entity = Succession
    label = "Passif propre"
    definition_period = ETERNITY

class role_succession(Variable):
    value_type = Enum
    possible_values = TypesRoleSuccession
    default_value = TypesRoleSuccession.succedant
    entity = Individu
    label = "Role de l'individu dans la succession"
    definition_period = ETERNITY

# class quidon(Variable):
#     value_type = Enum
#     possible_values = TypesQUIDON
#     default_value = TypesQUIDON.donateur
#     entity = Individu
#     label = "Role de l'individu dans la donation"
#

class role_representant(Variable):
    value_type = Enum
    possible_values = TypesRoleRepresentant
    default_value = TypesRoleRepresentant.decede
    entity = Individu
    label = "Rôle de l'individu par rapport au représenté"
    definition_period = ETERNITY

#class id(Variable):
#    value_type = str
#    entity = Individu
#    label = "Identifiant de l'individu"
#    definition_period = ETERNITY

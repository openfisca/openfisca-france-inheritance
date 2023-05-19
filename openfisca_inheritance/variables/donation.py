from openfisca_core.model_api import *

from openfisca_inheritance.entities import Individu, Succession  # Donations


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




# # class don_recu(Variable):
#     value_type = float
#     entity = Donations
#     label = "Don reçu"
#
# #    def function(self, actif_de_communaute, passif_de_communaute, actif_propre, passif_propre, assurance_vie):
# #        return (actif_de_communaute - passif_de_communaute) / 2 + actif_propre - passif_propre - assurance_vie
#     def formula(succession, period, parameters):
#
#         don = succession('don', period)
#         nombre_enfants_donataires = succession('nombre_enfants_donataires', period)
#         return don / nombre_enfants_donataires






#

# # class nombre_enfants_donataires(Variable):
#     value_type = float
#     entity = Donations
#     label = "Nombre d'enfants donataires"
#
#     def formula(succession, period, parameters):
#
#         is_enfant_donataire_holder = succession('is_enfant_donataire', period)
#         return self.sum_by_entity(is_enfant_donataire_holder)

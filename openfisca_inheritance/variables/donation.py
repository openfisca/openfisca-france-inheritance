from openfisca_core.model_api import *

from openfisca_inheritance.entities import Individu, donation  # Donations

from openfisca_inheritance.entities import Donation

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
#     def formula(donation, period, parameters):
#
#         don = donation('don', period)
#         nombre_enfants_donataires = donation('nombre_enfants_donataires', period)
#         return don / nombre_enfants_donataires

# class nombre_enfants_donataires(Variable):
#     value_type = float
#     entity = Donations
#     label = "Nombre d'enfants donataires"
#
#     def formula(donation, period, parameters):
#
#         is_enfant_donataire_holder = donation('is_enfant_donataire', period)
#         return self.sum_by_entity(is_enfant_donataire_holder)

class epoux_survivant(Variable):
    value_type = bool
    entity = Donation
    label = "Présence d'un époux survivant"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        return donation.nb_persons(donation.EPOUX_SURVIVANT)

class nombre_enfants(Variable):
    value_type = float
    entity = Donation
    label = "Nombre d'enfants"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        return donation.sum(donation.members('is_enfant', period))

class nombre_freres_soeurs(Variable):
    value_type = float
    entity = Donation
    label = "Nombre de frères et soeurs"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        return donation.sum(donation.members('is_freres_soeurs', period))

class nombre_autre(Variable):
    value_type = float
    entity = Donation
    label = "Nombre de tiers (personnes autre)"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        return donation.sum(donation.members('is_autre', period))
class part_epoux(Variable):
    value_type = float
    entity = Donation
    label = "Part epoux"
    definition_period = ETERNITY

class part_taxable(Variable):
    value_type = float
    entity = Donation
    label = "Part taxable"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        actif_imposable = donation('actif_imposable', period)
        nombre_enfants = donation('nombre_enfants', period)
        nombre_freres_soeurs = donation('nombre_freres_soeurs', period)

        abattement = parameters(period).abattement
        abattement_epoux_survivant = abattement.abattement_epoux.abattement_epoux_donation
        abattement_enfant = parameters(period).abattement.abattement_enfants.abattement_enfants_donation
        abattement_freres_soeurs = parameters(period).abattement.abattement_freres_soeurs

        epoux_survivant = donation('epoux_survivant', period)
        enfants = nombre_enfants > 0
        freres_soeurs = nombre_freres_soeurs > 0

        part_taxable_epoux_survivant = max_(actif_imposable - abattement_epoux_survivant, 0)
        part_taxable_enfant = max_(actif_imposable / (nombre_enfants + 1 * (nombre_enfants == 0)) - abattement_enfant, 0)
        part_taxable_freres_soeurs = max_(actif_imposable - abattement_freres_soeurs, 0)

        return select(
            [
                epoux_survivant > 0,
                enfants > 0,
                freres_soeurs > 0,
                ],
            [
                part_taxable_epoux_survivant,
                part_taxable_enfant,
                part_taxable_freres_soeurs,
                ],
            )
import itertools

from openfisca_core.model_api import *

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
class actif_de_communaute_don(Variable):
    value_type = float
    entity = Donation
    label = "Actif de Communauté"
    definition_period = ETERNITY

class actif_imposable_don(Variable):
    value_type = float
    entity = Donation
    label = "Actif imposable"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        part_epoux_don = donation('part_epoux_don', period)
        actif_de_communaute_don = donation('actif_de_communaute_don', period)
        passif_de_communaute_don = donation('passif_de_communaute_don', period)
        actif_propre_don = donation('actif_propre_don', period)
        passif_propre_don = donation('passif_propre_don', period)
        assurance_vie_don = donation('assurance_vie_don', period)
        return (
            (1 - part_epoux_don)
            * (
                (actif_de_communaute_don - passif_de_communaute_don) / 2
                + actif_propre_don
                - passif_propre_don
                - assurance_vie_don
                )
            )

class actif_propre_don(Variable):
    value_type = float
    entity = Donation
    label = "Actif propre"
    definition_period = ETERNITY

class assurance_vie_don(Variable):
    value_type = float
    entity = Donation
    label = "Assurance Vie"
    definition_period = ETERNITY

class epoux_survivant_don(Variable):
    value_type = bool
    entity = Donation
    label = "Présence d'un époux survivant"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        return donation.nb_persons(donation.EPOUX_SURVIVANT_DON)

class nombre_enfants_don(Variable):
    value_type = float
    entity = Donation
    label = "Nombre d'enfants"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        return donation.sum(donation.members('is_enfant', period))

class nombre_freres_soeurs_don(Variable):
    value_type = float
    entity = Donation
    label = "Nombre de frères et soeurs"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        return donation.sum(donation.members('is_freres_soeurs', period))

class part_epoux_don(Variable):
    value_type = float
    entity = Donation
    label = "Part epoux"
    definition_period = ETERNITY

class part_taxable_don(Variable):
    value_type = float
    entity = Donation
    label = "Part taxable"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        actif_imposable_don = donation('actif_imposable_don', period)
        nombre_enfants_don = donation('nombre_enfants_don', period)
        nombre_freres_soeurs_don = donation('nombre_freres_soeurs_don', period)

        abattement = parameters(period).abattement
        abattement_epoux_survivant = abattement.abattement_epoux.abattement_epoux_donation
        abattement_enfant = parameters(period).abattement.abattement_enfants.abattement_enfants_donation
        abattement_freres_soeurs = parameters(period).abattement.abattement_freres_soeurs

        epoux_survivant_don = donation('epoux_survivant_don', period)
        enfants = nombre_enfants_don > 0
        freres_soeurs = nombre_freres_soeurs_don > 0

        part_taxable_epoux_survivant_don = max_(actif_imposable_don - abattement_epoux_survivant, 0)
        part_taxable_enfant_don = max_(actif_imposable_don / (nombre_enfants_don + 1 * (nombre_enfants_don == 0)) - abattement_enfant, 0)
        part_taxable_freres_soeurs_don = max_(actif_imposable_don - abattement_freres_soeurs, 0)

        return select(
            [
                epoux_survivant_don> 0,
                enfants > 0,
                freres_soeurs > 0,
                ],
            [
                part_taxable_epoux_survivant_don,
                part_taxable_enfant_don,
                part_taxable_freres_soeurs_don,
                ],
        )

class passif_de_communaute_don(Variable):
    value_type = float
    entity = Donation
    label = "Passif de Communauté"
    definition_period = ETERNITY

class passif_propre_don(Variable):
    value_type = float
    entity = Donation
    label = "Passif propre"
    definition_period = ETERNITY
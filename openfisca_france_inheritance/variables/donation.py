from openfisca_core.model_api import *

from openfisca_france_inheritance.entities import Individu, Donation

# class date(Variable):
#     value_type = int
#     entity = Donations
#     label = "Année de la donation"
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

class don(Variable):
    value_type = float
    default_value = 0.0
    entity = Donation
    label = 'Montant de donation'
    definition_period = MONTH
    documentation = '''
        Articles 758 à 776 quater du Code général des impôts (CGI, 01/04/2025)
        Assiette des droits de mutation à titre gratuit : 
        https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069577/LEGISCTA000006191747/
    '''


class actif_de_communaute_don(Variable):
    value_type = float
    entity = Donation
    label = 'Actif de Communauté'
    definition_period = ETERNITY


class actif_imposable_don(Variable):
    value_type = float
    entity = Donation
    label = 'Actif imposable'
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
    label = 'Actif propre'
    definition_period = ETERNITY


class assurance_vie_don(Variable):
    value_type = float
    entity = Donation
    label = 'Assurance Vie'
    definition_period = ETERNITY


class epoux_donataire(Variable):
    value_type = bool
    entity = Donation
    label = "Présence d'un époux donataire"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        return donation.nb_persons(Donation.EPOUX_DONATAIRE)


class nombre_enfants_donataires(Variable):
    value_type = float
    entity = Donation
    label = "Nombre d'enfants donataires"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        return donation.sum(donation.members('is_enfant_donataire', period))


class nombre_freres_soeurs_donataires(Variable):
    value_type = float
    entity = Donation
    label = 'Nombre de frères et soeurs donataires'
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        return donation.sum(donation.members('is_frere_soeur_donataire', period))


class part_epoux_don(Variable):
    value_type = float
    entity = Donation
    label = 'Part époux donataire'
    definition_period = ETERNITY


class part_taxable_don(Variable):
    value_type = float
    entity = Donation
    label = "Part taxable d'une donation"
    definition_period = ETERNITY

    def formula(donation, period, parameters):
        actif_imposable_don = donation('actif_imposable_don', period)
        nombre_enfants_donataires = donation('nombre_enfants_donataires', period)
        nombre_freres_soeurs_donataires = donation('nombre_freres_soeurs_donataires', period)

        abattement = parameters(period).droits_mutation_titre_gratuit.abattement
        abattement_epoux_donataire = abattement.conjoint.donation
        abattement_enfants_donataires = abattement.enfants.donation
        abattement_freres_soeurs_donataires = abattement.adelphite

        epoux_donataire = donation('epoux_donataire', period)
        enfants_donataires = nombre_enfants_donataires > 0
        freres_soeurs_donataires = nombre_freres_soeurs_donataires > 0

        part_taxable_epoux_donataire = max_(actif_imposable_don - abattement_epoux_donataire, 0)
        part_taxable_enfants_donataires = max_(actif_imposable_don / (nombre_enfants_donataires + 1 * (nombre_enfants_donataires == 0)) - abattement_enfants_donataires, 0)
        part_taxable_freres_soeurs_donataires = max_(actif_imposable_don - abattement_freres_soeurs_donataires, 0)

        return select(
            [
                epoux_donataire > 0,
                enfants_donataires > 0,
                freres_soeurs_donataires > 0,
                ],
            [
                part_taxable_epoux_donataire,
                part_taxable_enfants_donataires,
                part_taxable_freres_soeurs_donataires,
                ],
            )


class passif_de_communaute_don(Variable):
    value_type = float
    entity = Donation
    label = 'Passif de communauté'
    definition_period = ETERNITY


class passif_propre_don(Variable):
    value_type = float
    entity = Donation
    label = 'Passif propre'
    definition_period = ETERNITY


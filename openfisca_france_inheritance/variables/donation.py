from openfisca_core.model_api import *

from openfisca_france_inheritance.entities import Donation

# class date(Variable):
#     value_type = int
#     entity = Donations
#     label = "Année de la donation"
#     definition_period = ETERNITY


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
    label = 'Part taxable'
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


class exoneration_don_familial(Variable):
    value_type = float
    default_value = 0.0
    entity = Donation
    label = "Montant de l'exonération pour don familial"
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048838931/2023-12-31/"
    documentation = '''
    Exonération pour don familial applicable si le donateur a moins de 80 ans et le donataire plus de 18 ans.
    '''


# TEMPORAIRE - formules initiales https://github.com/openfisca/openfisca-france-inheritance/pull/4 : 



class droits_mutation(Variable):
    value_type = float
    default_value = 0.0
    entity = Individu
    label = 'Droits de mutation à titre gratuit'
    definition_period = YEAR
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030061736'

    def formula_2015_01_01(individu, period, parameters):
        don = individu('don', period)
        lien_parente = individu('lien_parente', period)
        droit_exoneration_familial = individu(
            'droit_exoneration_familial', period)
        param = parameters(period).taxation_capital.donation

        def calc_droits(abattement, taux, bareme):
            exoneration_familial = param.exoneration_don_familial * droit_exoneration_familial
            base_imposable = max_(don - exoneration_familial - abattement, 0)
            if bareme:
                return bareme.calc(base_imposable)
            return taux * base_imposable

        montant_droits_donation = select(
            [
                (lien_parente == LienParente.aucun),
                (lien_parente == LienParente.quatrieme_degre),
                (lien_parente == LienParente.neveu),
                (lien_parente == LienParente.fratrie),
                (lien_parente == LienParente.ascendant),
                (lien_parente == LienParente.arriere_petit_enfant),
                (lien_parente == LienParente.petit_enfant),
                (lien_parente == LienParente.enfant),
                (lien_parente == LienParente.epoux_pacs),
                ],
            [
                calc_droits(0, param.taux_sans_parente, None),
                calc_droits(0, param.taux_parent_4eme_degre, None),
                calc_droits(param.abattement_neveu, param.taux_neveu, None),
                calc_droits(param.abattement_fratrie, 0, param.bareme_fratrie),
                calc_droits(param.abattement_ascendant, 0,
                            param.bareme_ligne_directe),
                calc_droits(param.abattement_arriere_petit_enfant,
                            0, param.bareme_ligne_directe),
                calc_droits(param.abattement_petit_enfant,
                            0, param.bareme_ligne_directe),
                calc_droits(param.abattement_enfant, 0,
                            param.bareme_ligne_directe),
                calc_droits(param.abattement_epoux_pacs,
                            0, param.bareme_epoux_pacs),
                ]
            )
        return montant_droits_donation



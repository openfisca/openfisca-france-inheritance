import itertools

from openfisca_core.model_api import *

from openfisca_inheritance.entities import Succession


class actif_de_communaute(Variable):
    value_type = float
    entity = Succession
    label = "Actif de Communauté"
    definition_period = ETERNITY


class actif_imposable(Variable):
    value_type = float
    entity = Succession
    label = "Actif imposable"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        part_epoux = succession('part_epoux', period)
        actif_de_communaute = succession('actif_de_communaute', period)
        passif_de_communaute = succession('passif_de_communaute', period)
        actif_propre = succession('actif_propre', period)
        passif_propre = succession('passif_propre', period)
        assurance_vie = succession('assurance_vie', period)
        return (
            (1 - part_epoux)
            * (
                (actif_de_communaute - passif_de_communaute) / 2
                + actif_propre
                - passif_propre
                - assurance_vie
                )
            )


class actif_propre(Variable):
    value_type = float
    entity = Succession
    label = "Actif propre"
    definition_period = ETERNITY


class actif_transmis(Variable):
    value_type = float
    entity = Succession
    label = "Actif transmis"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        # part_epoux = succession('part_epoux', period)
        actif_de_communaute = succession('actif_de_communaute', period)
        passif_de_communaute = succession('passif_de_communaute', period)
        actif_propre = succession('actif_propre', period)
        passif_propre = succession('passif_propre', period)

        return (
            (actif_de_communaute - passif_de_communaute) / 2
            + actif_propre
            - passif_propre
            )


class assurance_vie(Variable):
    value_type = float
    entity = Succession
    label = "Assurance Vie"
    definition_period = ETERNITY


class conjoint_survivant(Variable):
    value_type = bool
    entity = Succession
    label = "Présence d'un conjoint survivant"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        return succession.nb_persons(Succession.EPOUX_SURVIVANT)


class droits_sur_succession(Variable):
    value_type = float
    entity = Succession
    label = "Droits sur succession"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        return succession.sum(succession.members('droits', period))


class nombre_enfants(Variable):
    value_type = float
    entity = Succession
    label = "Nombre d'enfants"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        return succession.sum(succession.members('is_enfant', period))

class nombre_adelphite(Variable):
    value_type = float
    entity = Succession
    label = "Nombre de frères et soeurs"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        return succession.sum(succession.members('is_adelphite', period))

class part_epoux(Variable):
    value_type = float
    entity = Succession
    label = "Part epoux"
    definition_period = ETERNITY


# # class part_taxable(Variable):
#    value_type = float
#    entity = Succession
#    label = "Droits de succession"
#
#    def function(self, actif_de_communaute, passif_de_communaute, actif_propre, passif_propre, assurance_vie):
#        return (actif_de_communaute - passif_de_communaute) / 2 + actif_propre - passif_propre - assurance_vie
#    def function(self, actif_imposable, nombre_enfants):
#        part_taxable = np.max(actif_imposable / nombre_enfants - 100000, 0)
#        return part_taxable


class part_recue(Variable):
    value_type = float
    entity = Succession
    label = "Part reçue"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        actif_imposable = succession('actif_imposable', period)
        nombre_enfants = succession('nombre_enfants', period)
        return actif_imposable / nombre_enfants


class part_taxable(Variable):
    value_type = float
    entity = Succession
    label = "Part taxable"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        actif_imposable = succession('actif_imposable', period)
        nombre_enfants = succession('nombre_enfants', period)
        nombre_adelphite = succession('nombre_adelphite', period)

        abattement = parameters(period).abattement
        abattement_conjoint_survivant = abattement.abattement_conjoint.abattement_conjoint_succession
        abattement_part_enfant = parameters(period).abattement.abattement_enfants.abattement_enfants_succession
        abattement_adelphite= parameters(period).abattement.abattement_adelphite

        conjoint_survivant = succession('conjoint_survivant', period)
        enfants = nombre_enfants > 0
        adelphite = nombre_adelphite > 0

        part_taxable_conjoint_survivant = max_(actif_imposable - abattement_conjoint_survivant, 0)
        part_taxable_enfant = max_(actif_imposable / nombre_enfants - abattement_part_enfant, 0)
        part_taxable_enfant_0 = max_(actif_imposable - abattement_part_enfant, 0)
        part_taxable_adelphite = max_(actif_imposable - abattement_adelphite, 0)

        if nombre_enfants > 0:
            return select(
            [
                conjoint_survivant>0,
                enfants>0,
                adelphite>0
                ],
            [
                part_taxable_conjoint_survivant,
                part_taxable_enfant,
                part_taxable_adelphite
                ],
            )
        else:
            return select(
            [
                conjoint_survivant>0,
                enfants>0,
                adelphite>0
                ],
            [
                part_taxable_conjoint_survivant,
                part_taxable_enfant_0,
                part_taxable_adelphite
                ],
            )





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


class taux_sur_succession(Variable):
    value_type = float
    entity = Succession
    label = "Taux d'imposition sur la succession"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        droits_sur_succession = succession('droits_sur_succession', period)
        actif_imposable = succession('actif_imposable', period)
        taux_sur_succession = droits_sur_succession / actif_imposable
        return taux_sur_succession


class taux_sur_transmis(Variable):
    value_type = float
    entity = Succession
    label = "Taux d'imposition sur la succession"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        droits_sur_succession = succession('droits_sur_succession', period)
        actif_transmis = succession('actif_transmis', period)
        # assurance_vie = succession('assurance_vie', period)

        taux_sur_transmis = droits_sur_succession / actif_transmis
        return taux_sur_transmis

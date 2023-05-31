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
        abattement_par_part = parameters(period).abattement.abattement_enfants.abattement_enfants_succession
        return max_(actif_imposable / nombre_enfants - abattement_par_part, 0)


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

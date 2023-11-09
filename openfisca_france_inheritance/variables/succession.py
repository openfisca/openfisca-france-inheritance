import itertools

from openfisca_core.model_api import *

from openfisca_france_inheritance.entities import Succession


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


class epoux_survivant(Variable):
    value_type = bool
    entity = Succession
    label = "Présence d'un époux survivant"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        return succession.nb_persons(Succession.EPOUX_SURVIVANT)


class droits_sur_succession(Variable):
    value_type = float
    entity = Succession
    label = "Droits sur succession"
    definition_period = ETERNITY


    def formula(succession, period, parameters):

        bareme = parameters(period).bareme
        succession = bareme.bareme_ligne_directe

        return succession.sum(succession.members('droits', period))


class nombre_enfants(Variable):
    value_type = float
    entity = Succession
    label = "Nombre d'enfants"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        return succession.sum(succession.members('is_enfant', period))

class nombre_freres_soeurs(Variable):
    value_type = float
    entity = Succession
    label = "Nombre de frères et soeurs"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        return succession.sum(succession.members('is_frere_soeur', period))

class nombre_autre(Variable):
    value_type = float
    entity = Succession
    label = "Nombre de tiers (personnes autre)"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        return succession.sum(succession.members('is_autre', period))
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

    def formula_2008(succession, period, parameters):
        actif_imposable = succession('actif_imposable', period)
        nombre_enfants = succession('nombre_enfants', period)
        nombre_freres_soeurs = succession('nombre_freres_soeurs', period)
        nombre_autre = succession('nombre_autre',period)

        abattement = parameters(period).abattement
        abattement_enfant = abattement.abattement_enfants.abattement_enfants_succession
        abattement_freres_soeurs = abattement.abattement_freres_soeurs
        abattement_autre = abattement.abattement_autre_succession

        epoux_survivant = succession('epoux_survivant', period)
        enfants = nombre_enfants > 0
        freres_soeurs = nombre_freres_soeurs > 0
        autre = nombre_autre > 0

        part_taxable_epoux_survivant = 0
        part_taxable_enfant = max_(actif_imposable / (nombre_enfants + 1 * (nombre_enfants == 0)) - abattement_enfant, 0)
        part_taxable_freres_soeurs = max_(actif_imposable - abattement_freres_soeurs, 0)
        part_taxable_autre = max_(actif_imposable - abattement_autre, 0)

        return select(
            [
                epoux_survivant > 0,
                enfants > 0,
                freres_soeurs > 0,
                autre > 0,
                ],
            [
                part_taxable_epoux_survivant,
                part_taxable_enfant,
                part_taxable_freres_soeurs,
                part_taxable_autre,
                ],
            )

    def formula(succession, period, parameters):
        actif_imposable = succession('actif_imposable', period)
        nombre_enfants = succession('nombre_enfants', period)
        nombre_freres_soeurs = succession('nombre_freres_soeurs', period)
        nombre_autre = succession('nombre_autre',period)

        abattement = parameters(period).abattement
        abattement_epoux_survivant = abattement.abattement_epoux.abattement_epoux_succession
        abattement_enfant = abattement.abattement_enfants.abattement_enfants_succession
        abattement_freres_soeurs = abattement.abattement_freres_soeurs
        abattement_autre = abattement.abattement_autre_succession

        epoux_survivant = succession('epoux_survivant', period)
        enfants = nombre_enfants > 0
        freres_soeurs = nombre_freres_soeurs > 0
        autre = nombre_autre > 0

        part_taxable_epoux_survivant = max_(actif_imposable - abattement_epoux_survivant, 0)
        part_taxable_enfant = max_(actif_imposable / (nombre_enfants + 1 * (nombre_enfants == 0)) - abattement_enfant, 0)
        part_taxable_freres_soeurs = max_(actif_imposable - abattement_freres_soeurs, 0)
        part_taxable_autre = max_(actif_imposable - abattement_autre, 0)

        return select(
            [
                epoux_survivant > 0,
                enfants > 0,
                freres_soeurs > 0,
                autre > 0,
                ],
            [
                part_taxable_epoux_survivant,
                part_taxable_enfant,
                part_taxable_freres_soeurs,
                part_taxable_autre,
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

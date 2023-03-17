import itertools
from numpy import empty, maximum as max_

from openfisca_core.model_api import *
from openfisca_inheritance.entities import Individu, Succession  # Donations
# from openfisca_inheritance.variables.input_variables import DECEDE, ENFANT, EPOUX, PARENT


class actif_imposable(Variable):
    value_type = float
    entity = Succession
    label = "Actif imposable"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        period = period.start.offset('first-of', 'year').period('year')
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


class actif_transmis(Variable):
    value_type = float
    entity = Succession
    label = "Actif transmis"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        period.start.offset('first-of', 'year').period('year')
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


class degre_parente_civil(Variable):
    value_type = int
    entity = Individu
    label = "Degré de parenté, en droit civil, avec le décédé"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        index_represente = succession('index_represente', period)
        role_representant = succession('role_representant', period)

        holder = self.holder
        value_type = holder.column
        degre_parente = empty(holder.entity.count, dtype = column.dtype)
        degre_parente.fill(-9999)

        # Initialise les décédes à 0.
        degre_parente[role_representant == DECEDE] = 0

        # Mets les époux des décédés à -1
        degre_parente_represente = degre_parente[index_represente]
        degre_parente[(role_representant == EPOUX) & (degre_parente_represente >= 0)] = -1

        for i in itertools.count(0):
            degre_parente_represente = degre_parente[index_represente]
            degre_parente_precedent = degre_parente.copy()
            masque = ((role_representant == ENFANT) | (role_representant == PARENT)) & (degre_parente_represente >= i)
            degre_parente[masque] = degre_parente_represente[masque] + 1
            if (degre_parente == degre_parente_precedent).all():
                break

        return degre_parente


# # class degre_parente_fiscal(Variable):
#     value_type = int
#     entity = Individu
#     label = "Degré de parenté, en droit fiscal, avec le décédé"
#     definition_period = ETERNITY
#
#     def formula(succession, period, parameters):
#
#         return degre_parente


# # class don_recu(Variable):
#     value_type = float
#     entity = Donations
#     label = "Don reçu"
#
# #    def function(self, actif_de_communaute, passif_de_communaute, actif_propre, passif_propre, assurance_vie):
# #        return (actif_de_communaute - passif_de_communaute) / 2 + actif_propre - passif_propre - assurance_vie
#     def formula(succession, period, parameters):
#         period = period.start.offset('first-of', 'year').period('year')
#         don = succession('don', period)
#         nombre_enfants_donataires = succession('nombre_enfants_donataires', period)
#         return don / nombre_enfants_donataires


class droits_sur_succ(Variable):
    value_type = float
    entity = Succession
    label = "Droits sur succession"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        period = period.start.offset('first-of', 'year').period('year')
        droits = succession('droits', period)
        droits_sur_succ = self.sum_by_entity(droits)
        return droits_sur_succ


class is_enfant(Variable):
    value_type = float
    entity = Individu
    label = "Est un enfant"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        period = period.start.offset('first-of', 'year').period('year')
        quisucc = succession('quisucc', period)
        return quisucc >= 100


class is_enfant_donataire(Variable):
    value_type = float
    entity = Individu
    label = "Est un enfant donataire"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        period = period.start.offset('first-of', 'year').period('year')
        quidon = succession('quidon', period)
        return quidon >= 100


class nombre_enfants(Variable):
    value_type = float
    entity = Succession
    label = "Nombre d'enfants"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        period = period.start.offset('first-of', 'year').period('year')
        is_enfant_holder = succession('is_enfant', period)
        return self.sum_by_entity(is_enfant_holder)


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
#
#    def get_output_period(self, period):
#        return period.start.offset('first-of', 'year').period('year')


# # class nombre_enfants_donataires(Variable):
#     value_type = float
#     entity = Donations
#     label = "Nombre d'enfants donataires"
#
#     def formula(succession, period, parameters):
#         period = period.start.offset('first-of', 'year').period('year')
#         is_enfant_donataire_holder = succession('is_enfant_donataire', period)
#         return self.sum_by_entity(is_enfant_donataire_holder)


class part_recue(Variable):
    value_type = float
    entity = Succession
    label = "Part reçue"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        period = period.start.offset('first-of', 'year').period('year')
        actif_imposable = succession('actif_imposable', period)
        nombre_enfants = succession('nombre_enfants', period)
        return actif_imposable / nombre_enfants


class part_taxable(Variable):
    value_type = float
    entity = Succession
    label = "Nombre d'enfants"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        period = period.start.offset('first-of', 'year').period('year')
        actif_imposable = succession('actif_imposable', period)
        nombre_enfants = succession('nombre_enfants', period)
        abattement_par_part = parameters(period).succession.ligne_directe.abattement
        return max_(actif_imposable / nombre_enfants - abattement_par_part, 0)


class taux_sur_part_recue(Variable):
    value_type = float
    entity = Individu
    label = "Taux d'imposition sur la part recue"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        period = period.start.offset('first-of', 'year').period('year')
        droits = succession('droits', period)
        part_recue_holder = succession('part_recue', period)
        taux_sur_part_recue = droits / self.cast_from_entity_to_roles(part_recue_holder)
        return taux_sur_part_recue


class droits(Variable):
    value_type = float
    entity = Individu
    label = "Droits sur parts"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        period = period.start.offset('first-of', 'year').period('year')
        part_taxable_holder = succession('part_taxable', period)
        is_enfant = succession('is_enfant', period)
        bareme = parameters(period).succession.ligne_directe.bareme
        part_taxable = self.cast_from_entity_to_roles(part_taxable_holder, entity = "succession") * is_enfant
        droits = bareme.calc(part_taxable)
        # print bareme
        return droits


class taux_sur_succ(Variable):
    value_type = float
    entity = Succession
    label = "Taux d'imposition sur la succession"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        period = period.start.offset('first-of', 'year').period('year')
        droits_sur_succ = succession('droits_sur_succ', period)
        actif_imposable = succession('actif_imposable', period)
        taux_sur_succ = droits_sur_succ / actif_imposable
        return taux_sur_succ


class taux_sur_transmis(Variable):
    value_type = float
    entity = Succession
    label = "Taux d'imposition sur la succession"
    definition_period = ETERNITY

    def formula(succession, period, parameters):
        # droits = succession('droits', period)
        droits_sur_succ = succession('droits_sur_succ', period)
        actif_transmis = succession('actif_transmis', period)
        # assurance_vie = succession('assurance_vie', period)

        taux_sur_transmis = droits_sur_succ / actif_transmis
        return taux_sur_transmis

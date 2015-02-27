# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import maximum as max_

from openfisca_core.columns import FloatCol
# from openfisca_core.enumerations import Enum
from openfisca_core.formulas import make_reference_formula_decorator, SimpleFormulaColumn

from .entities import Donations, entity_class_by_symbol, Individus, Successions


reference_formula = make_reference_formula_decorator(entity_class_by_symbol = entity_class_by_symbol)


@reference_formula
class actif_imposable(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Actif imposable"

#    def function(self, actif_de_communaute, passif_de_communaute, actif_propre, passif_propre, assurance_vie):
#        return (actif_de_communaute - passif_de_communaute) / 2 + actif_propre - passif_propre - assurance_vie
    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        part_epoux = simulation.calculate('part_epoux', period)
        actif_de_communaute = simulation.calculate('actif_de_communaute', period)
        passif_de_communaute = simulation.calculate('passif_de_communaute', period)
        actif_propre = simulation.calculate('actif_propre', period)
        passif_propre = simulation.calculate('passif_propre', period)
        assurance_vie = simulation.calculate('assurance_vie', period)
        return period, (1 - part_epoux) * (
            (actif_de_communaute - passif_de_communaute) / 2 +
            actif_propre - passif_propre - assurance_vie
            )


@reference_formula
class actif_transmis(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Actif transmis"

#    def function(self, actif_de_communaute, passif_de_communaute, actif_propre, passif_propre, assurance_vie):
#        return (actif_de_communaute - passif_de_communaute) / 2 + actif_propre - passif_propre - assurance_vie
    def function(self, simulation, period):
        period.start.offset('first-of', 'year').period('year')
        # part_epoux = simulation.calculate('part_epoux', period)
        actif_de_communaute = simulation.calculate('actif_de_communaute', period)
        passif_de_communaute = simulation.calculate('passif_de_communaute', period)
        actif_propre = simulation.calculate('actif_propre', period)
        passif_propre = simulation.calculate('passif_propre', period)

        return period, (
            (actif_de_communaute - passif_de_communaute) / 2 + actif_propre - passif_propre
            )


@reference_formula
class don_recu(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Donations
    label = u"Don reçu"

#    def function(self, actif_de_communaute, passif_de_communaute, actif_propre, passif_propre, assurance_vie):
#        return (actif_de_communaute - passif_de_communaute) / 2 + actif_propre - passif_propre - assurance_vie
    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        don = simulation.calculate('don', period)
        nombre_enfants_donataires = simulation.calculate('nombre_enfants_donataires', period)
        return period, don / nombre_enfants_donataires


@reference_formula
class droits_sur_succ(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Droits sur succession"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        droits = simulation.calculate('droits', period)
        droits_sur_succ = self.sum_by_entity(droits)
        return period, droits_sur_succ


@reference_formula
class is_enfant(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = "Est un enfant"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        quisucc = simulation.calculate('quisucc', period)
        return period, quisucc >= 100


@reference_formula
class is_enfant_donataire(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = "Est un enfant donataire"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        quidon = simulation.calculate('quidon', period)
        return period, quidon >= 100


@reference_formula
class nombre_enfants(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Nombre d'enfants"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        is_enfant_holder = simulation.calculate('is_enfant', period)
        return period, self.sum_by_entity(is_enfant_holder)


# @reference_formula
# class part_taxable(SimpleFormulaColumn):
#    column = FloatCol
#    entity_class = Successions
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


@reference_formula
class nombre_enfants_donataires(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Donations
    label = "Nombre d'enfants donataires"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        is_enfant_donataire_holder = simulation.calculate('is_enfant_donataire', period)
        return period, self.sum_by_entity(is_enfant_donataire_holder)


@reference_formula
class part_recue(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = u"Part reçue"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        actif_imposable = simulation.calculate('actif_imposable', period)
        nombre_enfants = simulation.calculate('nombre_enfants', period)
        return period, actif_imposable / nombre_enfants


@reference_formula
class part_taxable(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Nombre d'enfants"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        actif_imposable = simulation.calculate('actif_imposable', period)
        nombre_enfants = simulation.calculate('nombre_enfants', period)
        abattement_par_part = simulation.legislation_at(period).succession.ligne_directe.abattement
        return period, max_(actif_imposable / nombre_enfants - abattement_par_part, 0)


@reference_formula
class taux_sur_part_recue(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = "Taux d'imposition sur la part recue"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        droits = simulation.calculate('droits', period)
        part_recue_holder = simulation.calculate('part_recue', period)
        taux_sur_part_recue = droits / self.cast_from_entity_to_roles(part_recue_holder)
        return period, taux_sur_part_recue


@reference_formula
class droits(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = "Droits sur parts"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        part_taxable_holder = simulation.calculate('part_taxable', period)
        is_enfant = simulation.calculate('is_enfant', period)
        bareme = simulation.legislation_at(period).succession.ligne_directe.bareme
        part_taxable = self.cast_from_entity_to_roles(part_taxable_holder, entity = "succession") * is_enfant
        droits = bareme.calc(part_taxable)
        print bareme
        return period, droits


@reference_formula
class taux_sur_succ(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Taux d'imposition sur la succession"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        droits_sur_succ = simulation.calculate('droits_sur_succ', period)
        actif_imposable = simulation.calculate('actif_imposable', period)
        taux_sur_succ = droits_sur_succ / actif_imposable
        return taux_sur_succ


@reference_formula
class taux_sur_transmis(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Taux d'imposition sur la succession"

    def function(self, simulation, period):
        # droits = simulation.calculate('droits', period)
        droits_sur_succ = simulation.calculate('droits_sur_succ', period)
        actif_transmis = simulation.calculate('actif_transmis', period)
        # assurance_vie = simulation.calculate('assurance_vie', period)
        period = period.start.offset('first-of', 'year').period('year')

        taux_sur_transmis = droits_sur_succ / actif_transmis
        return taux_sur_transmis


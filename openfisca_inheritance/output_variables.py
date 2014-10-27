# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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

from openfisca_core.accessors import law
from openfisca_core.columns import FloatCol
#from openfisca_core.enumerations import Enum
from openfisca_core.formulas import make_reference_formula_decorator, SimpleFormulaColumn

from .entities import Donations, entity_class_by_symbol, Individus, Successions


reference_formula = make_reference_formula_decorator(entity_class_by_symbol = entity_class_by_symbol)


@reference_formula
class actif_imposable(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Actif imposable"
    period_unit = u'year'

#    def function(self, actif_de_communaute, passif_de_communaute, actif_propre, passif_propre, assurance_vie):
#        return (actif_de_communaute - passif_de_communaute) / 2 + actif_propre - passif_propre - assurance_vie
    def function(self, part_epoux, actif_de_communaute, passif_de_communaute,\
                 actif_propre, passif_propre, assurance_vie):
        return (1-part_epoux)*((actif_de_communaute - passif_de_communaute) / 2 \
                + actif_propre - passif_propre - assurance_vie)

    def get_output_period(self, period):
        return period


@reference_formula
class actif_transmis(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Actif transmis"
    period_unit = u'year'

#    def function(self, actif_de_communaute, passif_de_communaute, actif_propre, passif_propre, assurance_vie):
#        return (actif_de_communaute - passif_de_communaute) / 2 + actif_propre - passif_propre - assurance_vie
    def function(self, part_epoux, actif_de_communaute, passif_de_communaute,\
                 actif_propre, passif_propre):
        return ((actif_de_communaute - passif_de_communaute) / 2 \
                + actif_propre - passif_propre)

    def get_output_period(self, period):
        return period
        

@reference_formula
class don_recu(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Donations
    label = "Don reçu"
    period_unit = u'year'

#    def function(self, actif_de_communaute, passif_de_communaute, actif_propre, passif_propre, assurance_vie):
#        return (actif_de_communaute - passif_de_communaute) / 2 + actif_propre - passif_propre - assurance_vie
    def function(self, don, nombre_enfants_donataires):
        return don / nombre_enfants_donataires

    def get_output_period(self, period):
        return period


@reference_formula
class droits_sur_succ(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Droits sur succession"
    period_unit = u'year'

    def function(self, droits):
        droits_sur_succ = self.sum_by_entity(droits)
        return droits_sur_succ

    def get_output_period(self, period):
        return period


@reference_formula
class is_enfant(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = "Est un enfant"
    period_unit = u'year'

    def function(self, quisucc):
        return quisucc >= 100

    def get_output_period(self, period):
        return period


@reference_formula
class is_enfant_donataire(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = "Est un enfant donataire"
    period_unit = u'year'

    def function(self, quidon):
        return quidon >= 100

    def get_output_period(self, period):
        return period


@reference_formula
class nombre_enfants(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Nombre d'enfants"
    period_unit = u'year'

    def function(self, is_enfant_holder):
        return self.sum_by_entity(is_enfant_holder)

    def get_output_period(self, period):
        return period


@reference_formula
class nombre_enfants_donataires(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Donations
    label = "Nombre d'enfants donataires"
    period_unit = u'year'

    def function(self, is_enfant_donataire_holder):
        return self.sum_by_entity(is_enfant_donataire_holder)

    def get_output_period(self, period):
        return period


@reference_formula
class part_recue(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = u"Part reçue"
    period_unit = u'year'

    def function(self, actif_imposable, nombre_enfants):
        return actif_imposable / nombre_enfants

    def get_output_period(self, period):
        return period


@reference_formula
class part_taxable(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Nombre d'enfants"
    period_unit = u'year'

    def function(self, actif_imposable, nombre_enfants,
                 abattement_par_part = law.succession.ligne_directe.abattement):
        return max_(actif_imposable / nombre_enfants - abattement_par_part, 0)

    def get_output_period(self, period):
        return period


@reference_formula
class taux_sur_part_recue(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = "Taux d'imposition sur la part recue"
    period_unit = u'year'
    def function(self, droits, part_recue_holder):
        taux_sur_part_recue = droits / self.cast_from_entity_to_roles(part_recue_holder)
        return taux_sur_part_recue

    def get_output_period(self, period):
        return period

        
@reference_formula
class droits(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = "Droits sur parts"
    period_unit = u'year'

    def function(self, part_taxable_holder, is_enfant, 
                 bareme = law.succession.ligne_directe.bareme):  # TODO rework
        part_taxable = self.cast_from_entity_to_roles(part_taxable_holder) * is_enfant
        droits = bareme.calc(part_taxable)
        return droits

    def get_output_period(self, period):
        return period


@reference_formula
class taux_sur_succ(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Taux d'imposition sur la succession"
    period_unit = u'year'

    def function(self, droits, droits_sur_succ, actif_imposable):
        taux_sur_succ = droits_sur_succ / actif_imposable
        return taux_sur_succ

    def get_output_period(self, period):
        return period


@reference_formula
class taux_sur_transmis(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Successions
    label = "Taux d'imposition sur la succession"
    period_unit = u'year'

    def function(self, droits, droits_sur_succ, actif_transmis, assurance_vie):
        taux_sur_transmis = droits_sur_succ / actif_transmis
        return taux_sur_transmis

    def get_output_period(self, period):
        return period


#@reference_formula
#class part_taxable(SimpleFormulaColumn):
#    column = FloatCol
#    entity_class = Successions
#    label = "Droits de succession"
#    period_unit = u'year'
#
#    def function(self, actif_de_communaute, passif_de_communaute, actif_propre, passif_propre, assurance_vie):
#        return (actif_de_communaute - passif_de_communaute) / 2 + actif_propre - passif_propre - assurance_vie
#    def function(self, actif_imposable, nombre_enfants):
#        part_taxable = np.max(actif_imposable / nombre_enfants - 100000, 0)
#        return part_taxable
#
#    def get_output_period(self, period):
#        return period

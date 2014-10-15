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
from openfisca_core.formulas import SimpleFormula


from .base import reference_formula
from .entities import Individus, Successions


#@reference_formula
#class revenu_disponible(SimpleFormula):
#    column = FloatCol
#    entity_class = Individus
#    label = u"Revenu disponible"
#    period_unit = u'year'
#
#    def function(self, rsa, salaire_imposable):
#        return rsa + salaire_imposable * 0.7
#
#
#@reference_formula
#class rsa(SimpleFormula):
#    column = FloatCol
#    entity_class = Individus
#    label = u"RSA"
#    period_unit = u'month'
#
#    def function(self, salaire_imposable):
#        return (salaire_imposable < 500) * 333
#
#
#@reference_formula
#class salaire_imposable(SimpleFormula):
#    column = FloatCol
#    entity_class = Individus
#    label = u"Salaire imposable"
#    period_unit = u'year'
#
#    def function(self, salaire_net):
#        return salaire_net * 0.9
#
#
#@reference_formula
#class salaire_net(SimpleFormula):
#    column = FloatCol
#    entity_class = Individus
#    label = u"Salaire net"
#    period_unit = u'year'
#
#    def function(self, salaire_brut):
#        return salaire_brut * 0.8

        
@reference_formula
class actif_imposable(SimpleFormula):
    column = FloatCol
    entity_class = Successions
    label = "Actif imposable"
    period_unit = u'year'

#    def function(self, actif_de_communaute, passif_de_communaute, actif_propre, passif_propre, assurance_vie):
#        return (actif_de_communaute - passif_de_communaute) / 2 + actif_propre - passif_propre - assurance_vie
    def function(self, actif_propre, passif_propre, assurance_vie):
        return actif_propre - passif_propre - assurance_vie


@reference_formula
class is_enfant(SimpleFormula):
    column = FloatCol
    entity_class = Individus
    label = "Est un enfant"
    period_unit = u'year'
    def function(self, quisucc):
        return quisucc >= 2


@reference_formula
class nombre_enfants(SimpleFormula):
    column = FloatCol
    entity_class = Successions
    label = "Nombre d'enfants"
    period_unit = u'year'

    def function(self, is_enfant_holder):
        return self.sum_by_entity(is_enfant_holder)


@reference_formula
class part_taxable(SimpleFormula):
    column = FloatCol
    entity_class = Successions
    label = "Nombre d'enfants"
    period_unit = u'year'

    def function(self, actif_imposable, nombre_enfants,
                 abattement_par_part = law.succession.ligne_directe.abattement):
        return max_(actif_imposable / nombre_enfants - abattement_par_part, 0)


@reference_formula
class droits(SimpleFormula):
    column = FloatCol
    entity_class = Individus
    label = "Droits"
    period_unit = u'year'

    def function(self, part_taxable_holder, is_enfant, 
                 bareme = law.succession.ligne_directe.bareme):  # TODO rework
        part_taxable = self.cast_from_entity_to_roles(part_taxable_holder) * is_enfant
        droits = bareme.calc(part_taxable)
        return droits


#@reference_formula
#class part_taxable(SimpleFormula):
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
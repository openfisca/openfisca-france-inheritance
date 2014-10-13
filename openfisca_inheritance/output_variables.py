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


from openfisca_core.columns import FloatCol
from openfisca_core.formulas import SimpleFormula

from .base import reference_formula
from .entities import Individus


@reference_formula
class revenu_disponible(SimpleFormula):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu disponible"
    period_unit = u'year'

    def function(self, rsa, salaire_imposable):
        return rsa + salaire_imposable * 0.7


@reference_formula
class rsa(SimpleFormula):
    column = FloatCol
    entity_class = Individus
    label = u"RSA"
    period_unit = u'month'

    def function(self, salaire_imposable):
        return (salaire_imposable < 500) * 333


@reference_formula
class salaire_imposable(SimpleFormula):
    column = FloatCol
    entity_class = Individus
    label = u"Salaire imposable"
    period_unit = u'year'

    def function(self, salaire_net):
        return salaire_net * 0.9


@reference_formula
class salaire_net(SimpleFormula):
    column = FloatCol
    entity_class = Individus
    label = u"Salaire net"
    period_unit = u'year'

    def function(self, salaire_brut):
        return salaire_brut * 0.8
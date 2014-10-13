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


from openfisca_core.columns import EnumCol, FloatCol, IntCol

from .base import QUIFAM, QUIFOY, QUIMEN, reference_input_variable
from .entities import Individus, Successions


reference_input_variable(
    column = IntCol(is_period_invariant = True),    
    entity_class = Individus,
    label = u"Identifiant de la famille",
    name = 'idfam',
    )

reference_input_variable(
    column = IntCol(is_period_invariant = True),    
    entity_class = Individus,
    label = u"Identifiant du foyer",
    name = 'idfoy',
    )
    
reference_input_variable(
    column = IntCol(is_period_invariant = True),    
    entity_class = Individus,
    label = u"Identifiant du ménage",
    name = 'idmen',
    )

reference_input_variable(
    column = IntCol,
    entity_class = Individus,
    label = u"Numéro d'ordre individuel",
    name = 'noi',
    )

reference_input_variable(
    column = EnumCol(QUIFAM, is_period_invariant = True),    
    entity_class = Individus,
    label = u"Role dans la famille",
    name = 'quifam',
    )

reference_input_variable(
    column = EnumCol(QUIFOY, is_period_invariant = True),    
    entity_class = Individus,
    label = u"Role dans le foyer",
    name = 'quifoy',
    )

reference_input_variable(
    column = EnumCol(QUIMEN, is_period_invariant = True),    
    entity_class = Individus,
    label = u"Role dans le ménage",
    name = 'quimen',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = "Salaire brut",
    name = 'salaire_brut',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Successions,
    label = u"Actif de communauté",
    name = 'actif_de_communaute',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Successions,
    label = u"Passif de communauté",
    name = 'passif_de_communaute',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Successions,
    label = u"Actif propre",
    name = 'actif_propre',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Successions,
    label = u"Passif propre",
    name = 'passif_propre',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Successions,
    label = "Assurance Vie",
    name = 'assurance_vie',
    )
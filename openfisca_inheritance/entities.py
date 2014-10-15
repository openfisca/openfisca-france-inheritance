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


import collections

from openfisca_core import entities


class Individus(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    is_persons_entity = True
    key_plural = 'individus'
    key_singular = 'individu'
    label = u'Personne'
    name_key = 'nom_individu'
    symbol = 'ind'


class Successions(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    key_plural = 'successions'
    key_singular = 'succession'
    label = u'Déclaration de succession'
#    max_cardinality_by_role_key = {
#        'epoux_survivant': 1,
#        'enfants': 9,
#        'collateraux': 9,
#        'legataires': 9,
#        }
#    roles_key = ['epoux_survivant', 'enfants', 'collateraux', 'legataires']    
#    label_by_role_key = {
#        'epoux survivant': u'Epoux survivant',
#        'enfants': u'Enfants',
#        'collateraux': u'Collatéraux',
#        'legataires': u'Légataires',
#        }    
    symbol = 'succ'


entity_class_by_symbol = dict(
    ind = Individus,   
    succ = Successions,   
    )

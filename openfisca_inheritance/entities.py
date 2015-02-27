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
    index_for_person_variable_name = 'idsucc'
    key_plural = 'successions'
    key_singular = 'succession'
    label = u'Déclaration de succession'
    name_key = 'nom_succession'
    role_for_person_variable_name = 'quisucc'
    symbol = 'succ'

    def iter_member_persons_role_and_id(self, member):
        decede_id = member['decede']
        assert decede_id is not None
        yield 0, decede_id

        epoux_survivant_id = member.get('epoux_survivant')
        if epoux_survivant_id is not None:
            yield 1, epoux_survivant_id

        enfants_id = member.get('enfants')
        if enfants_id is not None:
            for enfant_role, enfant_id in enumerate(enfants_id, 100):
                yield enfant_role, enfant_id


# class Donations(entities.AbstractEntity):
#     column_by_name = collections.OrderedDict()
#     index_for_person_variable_name = 'iddon'
#     key_plural = 'donations'
#     key_singular = 'donation'
#     label = u'Donation'
# #    max_cardinality_by_role_key = {
# #        'epoux_survivant': 1,
# #        'enfants': 9,
# #        'collateraux': 9,
# #        'legataires': 9,
# #        }
#     name_key = 'nom_donation'
#     role_for_person_variable_name = 'quidon'
# #    roles_key = ['epoux_survivant', 'enfants', 'collateraux', 'legataires']
# #    label_by_role_key = {
# #        'epoux survivant': u'Epoux survivant',
# #        'enfants': u'Enfants',
# #        'collateraux': u'Collatéraux',
# #        'legataires': u'Légataires',
# #        }
#     symbol = 'don'
#
#     def iter_member_persons_role_and_id(self, member):
#         donateur_id = member['donateur']
#         assert donateur_id is not None
#         yield 0, donateur_id
#
# #        epoux_donataire_id = member.get('epoux donataire')
# #        if epoux_donataire_id is not None:
# #            yield 1, epoux_donataire_id
#
#         enfants_donataires_id = member.get('enfants donataires')
#         if enfants_donataires_id is not None:
#             for enfant_role, enfant_id in enumerate(enfants_donataires_id, 100):
#                 yield enfant_role, enfant_id


entity_class_by_symbol = dict(
    ind = Individus,
    succ = Successions,
    # don = Donations,
    )

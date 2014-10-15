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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import collections
import datetime
import itertools
import logging
import numpy as np
import re
import uuid

from openfisca_core import conv, periods, scenarios, simulations


log = logging.getLogger(__name__)
N_ = lambda message: message


class Scenario(scenarios.AbstractScenario):
    def fill_simulation(self, simulation):
        entity_by_key_plural = simulation.entity_by_key_plural
        simulation.steps_count = steps_count = 1
        column_by_name = self.tax_benefit_system.column_by_name
        test_case = self.test_case

        individus = entity_by_key_plural[u'individus']
        individus.step_size = len(test_case[u'individus'])
        individus.count = steps_count * individus.step_size
        successions = entity_by_key_plural[u'successions']
        successions.step_size = len(test_case[u'successions'])
        successions.count = steps_count * successions.step_size

        individu_index_by_id = dict(
            (individu_id, individu_index)
            for individu_index, individu_id in enumerate(test_case[u'individus'].iterkeys())
            )
            
        individus.get_or_new_holder('id').array = np.array(
             [
                 individu_id + (u'-{}'.format(step_index) if step_index > 0 else u'')
                 for step_index in range(steps_count)
                 for individu_index, individu_id in enumerate(test_case[u'individus'].iterkeys())
                 ],
             dtype = object)

        individus.get_or_new_holder('idsucc').array = idsucc_array = np.empty(steps_count * individus.step_size,
            dtype = column_by_name['idsucc'].dtype)
        individus.get_or_new_holder('quisucc').array = quisucc_array = np.empty(steps_count * individus.step_size,
            dtype = column_by_name['quisucc'].dtype)
        successions_roles_count = 0
        for succession_index, succession in enumerate(test_case[u'successions'].itervalues()):
            decede_id = succession['decede']
            epoux_survivant_id = succession.get('epoux_survivant')
            enfants_id = succession.get('enfants', [])

            for step_index in range(steps_count):
                decede_index = individu_index_by_id[decede_id]
                idsucc_array[step_index * individus.step_size + decede_index] \
                    = step_index * successions.step_size + succession_index
                quisucc_array[step_index * individus.step_size + decede_index] = 0  # decede
                if epoux_survivant_id is not None:
                    epoux_survivant_index = individu_index_by_id[epoux_survivant_id]
                    idsucc_array[step_index * individus.step_size + epoux_survivant_index] \
                        = step_index * successions.step_size + succession_index
                    quisucc_array[step_index * individus.step_size + epoux_survivant_index] \
                        = 1  # epoux_survivant
                succession_roles_count = 2
                for enfant_dans_succ_index, enfant_id in enumerate(enfants_id):
                    enfant_index = individu_index_by_id[enfant_id]
                    idsucc_array[step_index * individus.step_size + enfant_index] \
                        = step_index * successions.step_size + succession_index
                    quisucc_array[step_index * individus.step_size + enfant_index] \
                        = 2 + enfant_dans_succ_index  # enfant n
                    succession_roles_count += 1
                if succession_roles_count > successions_roles_count:
                    successions_roles_count = succession_roles_count
        successions.roles_count = successions_roles_count

        self.set_simulation_variables(simulation)

    def init_simple_succession(self, decede = None, enfants = None,
                               epoux_survivant = None, succession = None, year = None):
        assert decede is not None
        assert enfants
        assert year is not None
        individus = []
        succession = {} if succession is None else succession.copy()
        id = succession.get('id')
        if id is None:
            succession['id'] = 'succ0'
        for index, individu in enumerate([decede, epoux_survivant] + enfants):
            if individu is None:
                continue
            id = individu.get('id')
            if id is None:
                individu = individu.copy()
                individu['id'] = id = 'ind{}'.format(index)
            individus.append(individu)
            if index == 0:
                succession['decede'] = individu['id']
            elif index == 1:
                succession['epoux_survivant'] = individu['id']
            else:
                succession.setdefault('enfants', []).append(individu['id'])

        self.period = periods.period('year', year)
        self.test_case = {
            'individus': collections.OrderedDict((
                (individu['id'], individu)
                for individu in individus
                )),
            'successions': collections.OrderedDict((
                (succession['id'], succession),
                )),
            }

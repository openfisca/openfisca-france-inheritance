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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import collections
import logging
import numpy as np

from openfisca_core import periods, scenarios


log = logging.getLogger(__name__)
N_ = lambda message: message


class Scenario(scenarios.AbstractScenario):
    def fill_simulation(self, simulation, variables_name_to_skip = None):
        if variables_name_to_skip is None:
            variables_name_to_skip = set()
        variables_name_to_skip.add('id')
        super(Scenario, self).fill_simulation(simulation, variables_name_to_skip = variables_name_to_skip)

        entity_by_key_plural = simulation.entity_by_key_plural
        individus = entity_by_key_plural[u'individus']
        steps_count = simulation.steps_count
        test_case = self.test_case
        individus.get_or_new_holder('id').array = np.array(
            [
                individu['id'] + (u'-{}'.format(step_index) if step_index > 0 else u'')
                for step_index in range(steps_count)
                for individu_index, individu in enumerate(test_case[u'individus'])
                ],
            dtype = object)

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
            'individus': individus,
            'donations': [],
            'successions': [succession],
            }

    def init_simple_donation(self, donateur = None, enfants_donataires = None,
            epoux_donataire = None, donation = None, year = None):
        assert donateur is not None
        assert enfants_donataires
        assert year is not None
        individus = []
        donation = {} if donation is None else donation.copy()
        id = donation.get('id')
        if id is None:
            donation['id'] = 'don0'
        for index, individu in enumerate([donateur] + enfants_donataires):
            if individu is None:
                continue
            id = individu.get('id')
            if id is None:
                individu = individu.copy()
                individu['id'] = id = 'ind{}'.format(index)
            individus.append(individu)
            if index == 0:
                donation['donateur'] = individu['id']
            else:
                donation.setdefault('enfants_donataires', []).append(individu['id'])

        self.period = periods.period('year', year)
        self.test_case = {
            'individus': individus,
            'donations': [],
            'successions': [succession],
            }

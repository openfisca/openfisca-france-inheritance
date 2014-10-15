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
        simulation.steps_count = 1
        test_case = self.test_case

        individus = entity_by_key_plural[u'individus']
        individus.step_size = len(test_case[u'individus'])
        individus.count = simulation.steps_count * individus.step_size
        successions = entity_by_key_plural[u'successions']
        successions.step_size = len(test_case[u'successions'])
        successions.count = simulation.steps_count * successions.step_size

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
            'individus': {
                individu['id']: individu
                for individu in individus
                },
            'successions': {
                succession['id']: succession
                },
            }

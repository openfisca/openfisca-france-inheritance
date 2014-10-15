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
import functools

from openfisca_core.columns import reference_input_variable
from openfisca_core.enumerations import Enum
from openfisca_core.formulas import reference_formula


QUISUCC = Enum(['decede', 'epoux_survivant', 'enfant1', 'enfant2', 'enfant3', 'enfant4', 'enfant5',
             'enfant6', 'enfant7', 'enfant8', 'enfant9' ])

column_by_name = collections.OrderedDict()
prestation_by_name = collections.OrderedDict()


# Functions and decorators


reference_formula = reference_formula(prestation_by_name = prestation_by_name)


reference_input_variable = functools.partial(
    reference_input_variable,
    column_by_name = column_by_name,
    )

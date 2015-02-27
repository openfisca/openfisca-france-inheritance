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


import os

from openfisca_core import taxbenefitsystems

from . import input_variables, output_variables  # noqa
from . import entities, scenarios

project_dir = os.path.dirname(os.path.abspath(__file__))


def init_country():
    class TaxBenefitSystem(taxbenefitsystems.XmlBasedTaxBenefitSystem):
        """French Inheritance system"""
        entity_class_by_key_plural = {
            entity_class.key_plural: entity_class
            for entity_class in entities.entity_class_by_symbol.itervalues()
            }
        legislation_xml_file_path = os.path.join(project_dir, 'param.xml')
        Scenario = scenarios.Scenario

    return TaxBenefitSystem

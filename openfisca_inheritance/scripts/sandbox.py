#! /usr/bin/env python
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


from pprint import pprint
import openfisca_inheritance


TaxBenefitSystem = openfisca_inheritance.init_country()
tax_benefit_system = TaxBenefitSystem()
scenario = tax_benefit_system.new_scenario()
scenario.init_simple_succession(
    succession = dict(actif_propre = 100000000, part_epoux = 0.3),
    decede = {},
    epoux_survivant = {},    
    enfants = [
        {},
        {},
        {},
        {},
        ],
    year = 2014,
    )

#pprint(scenario.test_case)
simulation = scenario.new_simulation(debug = True)
#print 'id', simulation.get_holder('id').array
print 'quisucc', simulation.get_holder('quisucc').array
#print 'idsucc', simulation.get_holder('idsucc').array
#print 'actif_imposable', simulation.calculate("actif_imposable")
#print 'nombre_enfants', simulation.calculate("nombre_enfants")
print 'part_taxable', simulation.calculate("part_taxable")
print 'droits', simulation.calculate("droits")
print 'taux_sur_part_recue', simulation.calculate("taux_sur_part_recue")
print 'droits_sur_succ', simulation.calculate("droits_sur_succ")
print 'taux_sur_transmis', simulation.calculate("taux_sur_transmis")
#! /usr/bin/env python



from datetime import date
from pprint import pprint

import openfisca_inheritance


TaxBenefitSystem = openfisca_inheritance.init_country()
tax_benefit_system = TaxBenefitSystem()
# scenario = tax_benefit_system.new_scenario()
# scenario.init_simple_succession(
#     succession = dict(actif_propre = 1000000, part_epoux = 0.3),
# #    donation = dict(don = 50000, date = 2012),
#     decede = {},
#     epoux_survivant = {},
#     enfants = [
#         {},
#         {},
#         {},
#         {},
#         ],
#     year = 2014,
#     )
year = 2014
simulation = tax_benefit_system.init_single_succession(
    succession = dict(actif_propre = 1000000, part_epoux = 0.3),
    individus = [
        dict(id = "décédé", role_representant = 'décédé', date_deces = date(year, 1, 1)),
        dict(id = "épouse", role_representant = 'époux', id_represente = "décédé"),
        dict(id = "père", role_representant = 'parent', id_represente = "décédé", date_deces = date(year - 1, 1, 1)),
        dict(id = "frère1", role_representant = 'enfant', id_represente = "père"),
        dict(id = "frère2", role_representant = 'enfant', id_represente = "père", date_deces = date(year - 1, 1, 1)),
        dict(id = "neveu1", role_representant = 'enfant', id_represente = "frère2"),
        dict(id = "neveu2", role_representant = 'enfant', id_represente = "frère2"),
        ],
    year = year,
    )

print 'role_representant', simulation.calculate("role_representant")
print 'id_represente', simulation.calculate("id_represente")
print 'date_deces', simulation.calculate("date_deces")
print 'degre_parente_civil', simulation.calculate("degre_parente_civil")

#print 'id', simulation.get_holder('id').array
#print 'quisucc', simulation.get_holder('quisucc').array
#print 'idsucc', simulation.get_holder('idsucc').array
print 'actif_imposable', simulation.calculate("actif_imposable")
print 'nombre_enfants', simulation.calculate("nombre_enfants")
print 'part_taxable', simulation.calculate("part_taxable")
print 'droits', simulation.calculate("droits")
#print 'taux_sur_part_recue', simulation.calculate("taux_sur_part_recue")
#print 'droits_sur_succession', simulation.calculate("droits_sur_succession")
#print 'taux_sur_transmis', simulation.calculate("taux_sur_transmis")

#scenario_donation = tax_benefit_system.new_scenario()
#scenario_donation.init_simple_donation(
#    donation = dict(don = 100000000),
#    donateur = {},
#    enfants_donataires = [
#        {},
#        {},
#        {},
#        {},
#        ],
#    year = 2014,
#    )
#
##pprint(scenario.test_case)
#simulation_donation = scenario_donation.new_simulation(debug = True)
#print 'don_recu', simulation_donation.calculate("don_recu")

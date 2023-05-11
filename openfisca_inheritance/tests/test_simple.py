from openfisca_inheritance import CountryTaxBenefitSystem as TaxBenefitSystem



test_case = {
    'individus': {
        'papa': {},
        'maman': {},
        'riri': {},
        'fifi': {},
        'loulou': {},
        },
    'successions': {
        'suc0': {
            'decede': 'papa',
            'epoux_survivant': 'maman',
            'enfants_survivants': [
                'riri', 'fifi', 'loulou',
                ],
            'actif_propre': 1000000,
            'part_epoux': 0.3,
            },
        },
    "period": 2014
    }



tax_benefit_system = TaxBenefitSystem()
scenario = tax_benefit_system.new_scenario()
scenario.init_from_dict(test_case)
simulation = scenario.new_simulation(debug = True)
simulation.calculate("actif_imposable", period = 2014)
simulation.calculate("nombre_enfants", period = 2014)
# simulation.calculate("part_taxable", period = 2014)
# simulation.calculate("droits", period = 2014)

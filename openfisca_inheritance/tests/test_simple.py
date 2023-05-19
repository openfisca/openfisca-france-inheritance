from openfisca_inheritance import CountryTaxBenefitSystem as TaxBenefitSystem


test_case = {
    'individus': {
        'papa': {},
        'maman': {},
        'riri': {
            "role_succession":
                {2014: "succedant"},
            "role_representant":
                {2014: "enfant"},
            },
        'fifi': {
            "role_succession":
                {2014: "succedant"},
            "role_representant":
                {2014: "enfant"},
            },
        'loulou': {
            "role_succession":
                {2014: "succedant"},
            "role_representant":
                {2014: "enfant"},
            },
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
simulation.calculate("role_succession", period = 2014)
simulation.calculate("is_enfant", period = 2014)
simulation.calculate("nombre_enfants", period = 2014)
# simulation.calculate("part_taxable", period = 2014)
# simulation.calculate("droits", period = 2014)




import openfisca_inheritance


def test_celib():
    TaxBenefitSystem = openfisca_inheritance.init_country()
    tax_benefit_system = TaxBenefitSystem()
    scenario = tax_benefit_system.new_scenario()
    scenario.init_simple_succession(
        decede = dict(
            actif_propre = 250000,
            ),
        enfants = [
            {},
            ],
        year = 2014,
        )
    scenario.new_simulation(debug = True)

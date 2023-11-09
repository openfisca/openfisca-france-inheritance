import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_france_inheritance.entities import entities

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


class CountryTaxBenefitSystem(TaxBenefitSystem):
    '''French inheritance tax benefit system.'''

    def __init__(self):
        TaxBenefitSystem.__init__(self, entities)
        parameters = os.path.join(COUNTRY_DIR, 'parameters', 'droits_mutation_titre_gratuit')
        self.load_parameters(parameters)
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))

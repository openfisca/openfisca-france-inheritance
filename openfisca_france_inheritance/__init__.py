import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_france_inheritance.entities import entities
from openfisca_france_inheritance.situation_examples import donation

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


class CountryTaxBenefitSystem(TaxBenefitSystem):
    '''French inheritance tax benefit system.'''

    def __init__(self):
        TaxBenefitSystem.__init__(self, entities)

        parameters = os.path.join(COUNTRY_DIR, 'parameters')
        self.load_parameters(parameters)

        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))

        self.open_api_config = {
            'variable_example': 'droits_mutation',
            'parameter_example': 'droits_mutation_titre_gratuit.exoneration.exoneration_don_familial',
            'simulation_example': donation,
        }

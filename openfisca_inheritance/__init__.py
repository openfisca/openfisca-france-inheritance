import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_inheritance.entities import entities
# from openfisca_inheritance.conf.cache_blacklist import cache_blacklist as conf_cache_blacklist


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


# def build_baremes(parameters)



class CountryTaxBenefitSystem(TaxBenefitSystem):
    """French inheritance tax benefit system."""

    def __init__(self):
        TaxBenefitSystem.__init__(self, entities)
        parameters = os.path.join(COUNTRY_DIR, 'parameters', 'droits_mutation_titre_gratuit')
        self.load_parameters(parameters)
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))


        # build_baremes(self.parameters)

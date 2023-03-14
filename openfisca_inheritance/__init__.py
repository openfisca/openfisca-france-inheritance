import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_france import entities
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales import preprocessing
from openfisca_france.conf.cache_blacklist import cache_blacklist as conf_cache_blacklist
from openfisca_france.situation_examples import couple


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


class CountryTaxBenefitSystem(TaxBenefitSystem):
    """French inheritance tax benefit system."""

    def __init__(self):
        super(CountryTaxBenefitSystem, self).__init__(self, entities.entities)
        parameters = os.path.join(COUNTRY_DIR, 'parameters')
        self.load_parameters(parameters)
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))

from openfisca_france.model.base import *


class don(Variable):
    value_type = float
    default_value = 0.0
    entity = Individu
    label = 'Montant de donation'
    definition_period = YEAR
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030061736'


class droits_mutation(Variable):
    value_type = float
    default_value = 0.0
    entity = Individu
    label = 'Droits de mutation à titre gratuit'
    definition_period = YEAR
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030061736'

    def formula_2015_01_01(individu, period, parameters):
        don = individu('don', period)
        taux = parameters(period).taxation_capital.donation.taux_sans_parente
        return don * taux

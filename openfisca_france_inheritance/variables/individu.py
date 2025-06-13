from openfisca_core.model_api import *

from openfisca_france_inheritance.entities import Donation, Individu, Succession


class date_deces(Variable):
    value_type = date
    entity = Individu
    label = 'Date du décès'
    definition_period = ETERNITY


class TypesRoleRepresentant(Enum):
    __order__ = 'decede enfant epoux parent freres_soeurs'  # Needed to preserve the enum order in Python 2
    decede = 'Personne décédée'
    # donateur = 'Personne donatrice'
    enfant = 'Enfant'
    epoux = 'Époux'
    parent = 'Parent'
    freres_soeurs = 'Frères et Soeurs'


class date_donation(Variable):
    value_type = date
    entity = Individu
    label = 'Date de la donation'
    definition_period = ETERNITY


# class degre_parente_civil(Variable):
#     value_type = int
#     entity = Individu
#     label = 'Degré de parenté, en droit civil, avec le décédé'
#     definition_period = ETERNITY

#     def formula(succession, period, parameters):
#         index_represente = succession('index_represente', period)
#         role_representant = succession('role_representant', period)

#         holder = self.holder
#         value_type = holder.column
#         degre_parente = empty(holder.entity.count, dtype = column.dtype)
#         degre_parente.fill(-9999)

#         # Initialise les décédes à 0.
#         degre_parente[role_representant == DECEDE] = 0

#         # Mets les époux des décédés à -1
#         degre_parente_represente = degre_parente[index_represente]
#         degre_parente[(role_representant == EPOUX) & (degre_parente_represente >= 0)] = -1

#         for i in itertools.count(0):
#             degre_parente_represente = degre_parente[index_represente]
#             degre_parente_precedent = degre_parente.copy()
#             masque = ((role_representant == ENFANT) | (role_representant == PARENT)) & (degre_parente_represente >= i)
#             degre_parente[masque] = degre_parente_represente[masque] + 1
#             if (degre_parente == degre_parente_precedent).all():
#                 break

#         return degre_parente


# # class degre_parente_fiscal(Variable):
#     value_type = int
#     entity = Individu
#     label = 'Degré de parenté, en droit fiscal, avec le décédé'
#     definition_period = ETERNITY
#
#     def formula(succession, period, parameters):
#
#         return degre_parente


class droits(Variable):
    value_type = float
    entity = Individu
    label = 'Droits sur parts'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        part_taxable = individu.succession('part_taxable', period)
        dmtg = parameters(period).droits_mutation_titre_gratuit
        bareme = dmtg.bareme.ligne_directe
        droits = bareme.calc(part_taxable)
        return droits


class id(Variable):
    value_type = str
    entity = Individu
    label = "Identifiant de l'individu"
    definition_period = ETERNITY


class id_represente(Variable):
    value_type = str
    entity = Individu
    label = "Identifiant de l'individu représenté par cet individu"
    definition_period = ETERNITY


class iddon(Variable):
    value_type = int
    entity = Individu
    label = "Donation auquel appartient l'individu"
    definition_period = ETERNITY


class idsucc(Variable):
    value_type = int
    entity = Individu
    label = "Succession auquel appartient l'individu"
    definition_period = ETERNITY


class index_represente(Variable):
    value_type = int
    entity = Individu
    label = "Index de l'individu représenté par cet individu"
    definition_period = ETERNITY


class is_donateur(Variable):
    value_type = bool
    entity = Individu
    label = 'Est donateur'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Donation.DONATEUR)


class is_enfant(Variable):
    value_type = bool
    entity = Individu
    label = 'Est un enfant'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Succession.ENFANT_SURVIVANT)


class is_enfant_donataire(Variable):
    value_type = float
    entity = Individu
    label = 'Est un enfant donataire'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Donation.ENFANT_DONATAIRE)


class is_frere_soeur(Variable):
    value_type = bool
    entity = Individu
    label = 'Est une soeur ou un frère'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Succession.FRERE_SOEUR)


class is_frere_soeur_donataire(Variable):
    value_type = bool
    entity = Individu
    label = 'Est une soeur ou un frère donataire'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Donation.FRERE_SOEUR_DONATAIRE)


class is_autre(Variable):
    value_type = bool
    entity = Individu
    label = 'Est une personnes en dehors du cercle familiale (un tiers)'
    definition_period = ETERNITY

    def formula(individu, period, parameters):
        return individu.has_role(Succession.AUTRE_SURVIVANT)

# class quidon(Variable):
#     value_type = Enum
#     possible_values = TypesQUIDON
#     default_value = TypesQUIDON.donateur
#     entity = Individu
#     label = 'Role de l'individu dans la donation'
#


class role_representant(Variable):
    value_type = Enum
    possible_values = TypesRoleRepresentant
    default_value = TypesRoleRepresentant.decede
    entity = Individu
    label = "Rôle de l'individu par rapport au représenté"
    definition_period = ETERNITY


class taux_sur_part_recue(Variable):
    value_type = float
    entity = Individu
    label = "Taux d'imposition sur la part recue"
    definition_period = ETERNITY

    def formula(indvidu, period, parameters):
        droits = indvidu('droits', period)
        part_recue = indvidu('part_recue', period)
        taux_sur_part_recue = droits / part_recue
        return taux_sur_part_recue
